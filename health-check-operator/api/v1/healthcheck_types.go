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

package v1

import (
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// HealthCheckSpec defines the desired state of HealthCheck
type HealthCheckSpec struct {
	ID                     string `json:"id,omitempty"`
	Name                   string `json:"name,omitempty"`
	URI                    string `json:"uri,omitempty"`
	IsPaused               bool   `json:"isPaused,omitempty"`
	NumRetries             int    `json:"numRetries,omitempty"`
	UptimeSLA              int    `json:"uptimeSLA,omitempty"`
	ResponseTimeSLA        int    `json:"responseTimeSLA,omitempty"`
	UseSSL                 bool   `json:"useSSL,omitempty"`
	ResponseStatusCode     int    `json:"responseStatusCode,omitempty"`
	CheckIntervalInSeconds int    `json:"checkIntervalInSeconds,omitempty"`
	CheckCreated           string `json:"checkCreated,omitempty"`
	CheckUpdated           string `json:"checkUpdated,omitempty"`
}

// HealthCheckStatus defines the observed state of HealthCheck
type HealthCheckStatus struct {
	LastExecutionTime string                   `json:"lastExecutionTime,omitempty"`
	Status            string                   `json:"status,omitempty"`
	Active            []corev1.ObjectReference `json:"active,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status

// HealthCheck is the Schema for the healthchecks API
type HealthCheck struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   HealthCheckSpec   `json:"spec,omitempty"`
	Status HealthCheckStatus `json:"status,omitempty"`
}

//+kubebuilder:object:root=true

// HealthCheckList contains a list of HealthCheck
type HealthCheckList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []HealthCheck `json:"items"`
}

func init() {
	SchemeBuilder.Register(&HealthCheck{}, &HealthCheckList{})
}
