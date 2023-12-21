/*
Copyright 2023.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controller

import (
	"context"
	"encoding/json"
	"fmt"
	batchv1 "k8s.io/api/batch/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/utils/pointer"
	"math"
	"os"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/log"
	"time"
	webappv1 "webapp/api/v1"

	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// HealthCheckReconciler reconciles a HealthCheck object
type HealthCheckReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

//+kubebuilder:rbac:groups=webapp.vaibhavmahajan.in,namespace=health-check-operator-system,resources=healthchecks,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=webapp.vaibhavmahajan.in,namespace=health-check-operator-system,resources=healthchecks/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=webapp.vaibhavmahajan.in,namespace=health-check-operator-system,resources=healthchecks/finalizers,verbs=update
//+kubebuilder:rbac:groups=batch,resources=jobs,namespace=health-check-operator-system,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=batch,resources=cronjobs,namespace=health-check-operator-system,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=batch,resources=jobs/status,namespace=health-check-operator-system,verbs=get
//+kubebuilder:rbac:groups="",namespace=health-check-operator-system,resources=pods;pods/log,verbs=get;list;watch

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// the HealthCheck object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.16.3/pkg/reconcile
func (r *HealthCheckReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	logger := log.FromContext(ctx)
	// name of our custom finalizer
	myFinalizer := "batch.tutorial.kubebuilder.io/finalizer"

	// Get HealthCheck instances in the current namespace
	healthCheck := &webappv1.HealthCheck{}
	if err := r.Get(ctx, req.NamespacedName, healthCheck); err != nil {
		if errors.IsNotFound(err) {
			logger.Info("Health Check instance doesn't exist")
			return ctrl.Result{}, nil
		}
		logger.Error(err, "Failed to get HealthCheck instance")
		return ctrl.Result{}, nil
	}

	// Ensure the CronJob is in the same namespace as the operator
	if healthCheck.GetNamespace() != req.Namespace {
		logger.Info("Ignoring CronJob in a different namespace", "CronJob.Namespace", healthCheck.Namespace)
		return ctrl.Result{}, nil
	}

	minutes := int(math.Ceil(float64(healthCheck.Spec.CheckIntervalInSeconds) / 60.0))

	schedule := fmt.Sprintf("*/%d * * * *", minutes)

	imagePullSecretName := os.Getenv("IMAGE_PULL_SECRET_NAME")
	performHealthCheckImage := os.Getenv("PERFORM_HEALTH_CHECK_IMAGE")
	kafkaTopic := os.Getenv("KAFKA_TOPIC")
	kafkaNamespace := os.Getenv("KAFKA_NAMESPACE")

	cronJob := &batchv1.CronJob{
		ObjectMeta: metav1.ObjectMeta{
			Namespace: healthCheck.Namespace,
			Name:      healthCheck.Name + "-cronjob",
			OwnerReferences: []metav1.OwnerReference{
				{
					APIVersion:         healthCheck.APIVersion,
					Kind:               healthCheck.Kind,
					Name:               healthCheck.Name,
					UID:                healthCheck.UID,
					Controller:         pointer.Bool(true),
					BlockOwnerDeletion: pointer.Bool(true),
				},
			},
		},

		Spec: batchv1.CronJobSpec{
			Schedule:                   schedule,
			Suspend:                    pointer.Bool(healthCheck.Spec.IsPaused),
			SuccessfulJobsHistoryLimit: pointer.Int32(3),
			FailedJobsHistoryLimit:     pointer.Int32(1),
			JobTemplate: batchv1.JobTemplateSpec{
				ObjectMeta: metav1.ObjectMeta{
					Labels: map[string]string{
						"cronjob-name": healthCheck.Name + "-cronjob",
					},
				},
				Spec: batchv1.JobSpec{
					Template: corev1.PodTemplateSpec{
						ObjectMeta: metav1.ObjectMeta{
							Annotations: map[string]string{
								"proxy.istio.io/config": `{
										"holdApplicationUntilProxyStarts": true
								}`,
							},
						},
						Spec: corev1.PodSpec{
							RestartPolicy:      corev1.RestartPolicyOnFailure,
							ServiceAccountName: "health-check-operator-controller-manager",
							ImagePullSecrets: []corev1.LocalObjectReference{
								{Name: imagePullSecretName},
							},
							Containers: []corev1.Container{
								{
									Name:  healthCheck.Name + "-job",
									Image: performHealthCheckImage,
									Resources: corev1.ResourceRequirements{
										Limits: corev1.ResourceList{
											"cpu":    resource.MustParse("100m"),
											"memory": resource.MustParse("100Mi"),
										},
										Requests: corev1.ResourceList{
											"cpu":    resource.MustParse("50m"),
											"memory": resource.MustParse("50Mi"),
										},
									},
									Env: []corev1.EnvVar{
										{
											Name:  "KAFKA_TOPIC",
											Value: kafkaTopic,
										},
										{
											Name:  "HTTP_CHECK_DATA",
											Value: healthCheckToJSON(healthCheck),
										},
										{
											Name:  "KAFKA_NAMESPACE",
											Value: kafkaNamespace,
										},
									},
								},
							},
						},
					},
				},
			},
		},
	}

	// Finalizer: examine DeletionTimestamp to determine if object is under deletion
	if healthCheck.ObjectMeta.DeletionTimestamp.IsZero() {
		// The object is not being deleted, so if it does not have our finalizer,
		// then lets add the finalizer and update the object. This is equivalent
		// registering our finalizer.
		if !controllerutil.ContainsFinalizer(healthCheck, myFinalizer) {
			controllerutil.AddFinalizer(healthCheck, myFinalizer)
			if err := r.Update(ctx, healthCheck); err != nil {
				logger.Error(err, "Failed to update existing CR with finalizer", "HealthCheck.Name", healthCheck.Name)
				return ctrl.Result{}, err
			}
		}
	} else {
		// The object is being deleted
		if controllerutil.ContainsFinalizer(healthCheck, myFinalizer) {
			// our finalizer is present, so lets handle any external dependency
			if err := r.deleteExternalResources(ctx, healthCheck, cronJob); err != nil {
				// if fail to delete the external dependency here, return with error
				// so that it can be retried

				if errors.IsNotFound(err) {
					logger.Info("Already being deleted", "HealthCheck.Name", healthCheck.Name)
				} else {
					logger.Error(err, "Failed to delete external dependencies with finalizer", "HealthCheck.Name", healthCheck.Name)
					return ctrl.Result{}, err
				}

			}
			// remove our finalizer from the list and update it.
			controllerutil.RemoveFinalizer(healthCheck, myFinalizer)
			if err := r.Update(ctx, healthCheck); err != nil {
				logger.Error(err, "Failed to remove finalizer from CR", "HealthCheck.Name", healthCheck.Name)
				return ctrl.Result{}, err
			}
		}
		// Stop reconciliation as the item is being deleted
		return ctrl.Result{}, nil
	}

	existingCronJob := &batchv1.CronJob{}
	if err := r.Client.Get(ctx, client.ObjectKeyFromObject(cronJob), existingCronJob); err != nil {
		if errors.IsNotFound(err) {
			// CronJob doesn't exist, create it
			if createErr := r.Client.Create(ctx, cronJob); createErr != nil {
				logger.Error(createErr, "Failed to create CronJob", "HealthCheck.Name", healthCheck.Name)
				return ctrl.Result{}, createErr
			}
		} else {
			// Other error during Get operation
			logger.Error(err, "Failed to get existing CronJob", "HealthCheck.Name", healthCheck.Name)
			return ctrl.Result{}, err
		}
	} else {
		// CronJob exists, update it
		// Versions match, proceed with the update
		existingCronJob.Spec = cronJob.Spec
		if updateErr := r.Client.Update(ctx, existingCronJob, &client.UpdateOptions{}); updateErr != nil {
			logger.Error(updateErr, "Failed to update CronJob", "HealthCheck.Name", healthCheck.Name)
			return ctrl.Result{}, updateErr
		}
	}

	// Update HealthCheck status
	logger.Info("Updating status...")

	latestHealthCheck := &webappv1.HealthCheck{}
	if err := r.Client.Get(ctx, client.ObjectKeyFromObject(healthCheck), latestHealthCheck); err != nil {
		// Handle error (e.g., log and return)
		return ctrl.Result{}, err
	}

	maxRetries := 3
	// Retry reconciliation in case of conflict
	for retry := 0; retry < maxRetries; retry++ {
		if latestHealthCheck.ResourceVersion == healthCheck.ResourceVersion {
			// Versions match, proceed with the update
			if err := r.updateHealthCheckStatus(ctx, healthCheck, cronJob); err != nil {
				if errors.IsConflict(err) {
					// Conflict, retry reconciliation
					continue
				}
				logger.Error(err, "Failed to update HealthCheck status", "HealthCheck.Spec.Name", healthCheck.Name)
				return ctrl.Result{}, err
			}
		} else {
			// Versions don't match, handle the conflict (e.g., log and return)
			logger.Info("HealthCheck was modified by another update, skipping reconciliation", "HealthCheck.Spec.Name", healthCheck.Name)
		}
		break
	}

	return ctrl.Result{}, nil
}

func (r *HealthCheckReconciler) deleteExternalResources(ctx context.Context, healthCheck *webappv1.HealthCheck, cronJob *batchv1.CronJob) error {
	// delete any external resources associated with the cronJob

	var jobList batchv1.JobList
	if err := r.Client.List(ctx, &jobList, client.InNamespace(healthCheck.Namespace), client.MatchingLabels{"cronjob-name": cronJob.Name}); err != nil {
		return err
	}
	// Delete each associated Job
	for _, job := range jobList.Items {
		if err := r.Client.Delete(ctx, &job); err != nil {
			return err
		}
	}

	//Delete the cronJob
	if err := r.Client.Delete(ctx, cronJob); err != nil {
		return err
	}

	return nil
}

func (r *HealthCheckReconciler) updateHealthCheckStatus(ctx context.Context, healthCheck *webappv1.HealthCheck, cronJob *batchv1.CronJob) error {
	// Logic for updating HealthCheck status based on the last job run by the CronJob

	//logger := log.FromContext(ctx)
	var jobList batchv1.JobList
	if err := r.Client.List(ctx, &jobList, client.InNamespace(healthCheck.Namespace), client.MatchingLabels{"cronjob-name": cronJob.Name}); err != nil {
		return err
	}

	// Find the most recent job
	var mostRecentJob *batchv1.Job
	for _, job := range jobList.Items {
		if mostRecentJob == nil || job.CreationTimestamp.After(mostRecentJob.CreationTimestamp.Time) {
			mostRecentJob = &job
		}
	}

	if mostRecentJob != nil {
		// Now safely access the status of the most recent Job
		completionTime := mostRecentJob.Status.CompletionTime
		if completionTime != nil {
			lastExecutionTime := completionTime.Time.Format(time.RFC3339)
			healthCheck.Status.LastExecutionTime = lastExecutionTime
			healthCheck.Status.Status = getLastJobStatus(mostRecentJob)
			fmt.Println("Last Execution Time:", lastExecutionTime)
		} else {
			// Handle the case where the most recent Job has not completed yet
			healthCheck.Status.LastExecutionTime = ""
			healthCheck.Status.Status = "Not completed yet"
		}
	} else {
		// Handle the case where no Jobs are associated with the CronJob
		healthCheck.Status.LastExecutionTime = ""
		healthCheck.Status.Status = "No executions"
	}

	// Update the HealthCheck status in the cluster
	if err := r.Status().Update(ctx, healthCheck); err != nil {
		return err
	}

	return nil
}

func getLastJobStatus(job *batchv1.Job) string {
	if job.Status.Succeeded > 0 {
		return "Success"
	} else if job.Status.Failed > 0 {
		return "Failed"
	} else {
		return "Running"
	}
}

func healthCheckToJSON(healthCheck *webappv1.HealthCheck) string {
	data := map[string]interface{}{
		"num_retries":          healthCheck.Spec.NumRetries,
		"response_status_code": healthCheck.Spec.ResponseStatusCode,
		"uri":                  healthCheck.Spec.URI,
		"use_ssl":              healthCheck.Spec.UseSSL,
	}

	jsonData, _ := json.Marshal(data)
	return string(jsonData)
}

func (r *HealthCheckReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&webappv1.HealthCheck{}).
		Owns(&batchv1.CronJob{}).
		Complete(r)
}
