# Python Imports
import json
import os
from typing import Any

# Framework Imports
from fastapi import FastAPI, status, Request, HTTPException, Depends, Body
from sqlalchemy.orm import Session

# Project Imports
from utils import response
from logging.config import dictConfig
import logging
from log import LogConfig
from database import database_connection, get_db
from schema import HttpCheck
import models
from kubernetes import config, client

dictConfig(LogConfig().dict())
logger = logging.getLogger("cloud")

app = FastAPI()


@app.exception_handler(exc_class_or_status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
async def handle_method_not_allowed(request: Request, exc: HTTPException):
    """Handle Method Not Allowed Exception.

    Args:
        request (Request): The incoming request.
        exc (HTTPException): The exception instance.

    Returns:
        JSONResponse: Response indicating Method Not Allowed.
    """
    return response("Method Not Allowed", status.HTTP_405_METHOD_NOT_ALLOWED, no_content=True)


@app.get("/healthz")
async def health_check(payload: Any = Body(None)):
    """Health Check Endpoint.

    Args:
        payload (Any, optional): Payload to be checked. Defaults to None.

    Returns:
        JSONResponse: Health check response.
    """
    if payload:
        return response("Request cannot contain payload", status.HTTP_400_BAD_REQUEST, no_content=True)
    if not database_connection():
        return response("Database is not connected", status.HTTP_503_SERVICE_UNAVAILABLE, no_content=True)
    return response("Database is connected", status.HTTP_200_OK, log_level="info", no_content=True)


@app.get("/")
async def probe():
    """Probe Endpoint.

    Returns:
        JSONResponse: Probe response.
    """
    return response("Application is running", status.HTTP_200_OK, log_level="info", no_content=True)


def get_crd_data():
    """Get Custom Resource Definition (CRD) Data.

    Returns:
        dict: CRD data including group, version, api_version, kind, and plural.
    """

    try:
        # config.load_kube_config() # Uncomment this for local developement
        config.load_incluster_config() # For cluster deployment
        api_crd = client.ApiextensionsV1Api()
        crds = api_crd.read_custom_resource_definition(name=os.getenv("HEALTH_CHECK_NAME"))
        group = crds.spec.group
        version = crds.spec.versions[0].name
        api_version = "{}/{}".format(group, version)
        kind = crds.spec.names.kind
        plural = crds.spec.names.plural

        data = {"group": group, "version": version, "api_version": api_version, "kind": kind, "plural": plural}
        logger.info("Data read successful")
        logger.info("Data: {}".format(data))

        return data
    except Exception as e:
        logger.error(str(e))
        return None
    


# Create HTTP-Check
@app.post("/v1/http-check")
async def create_http_check(http_check: HttpCheck, db: Session = Depends(get_db)):
    """Create HTTP Check Endpoint.

    Args:
        http_check (HttpCheck): The HTTP Check data.
        db (Session): The database session.

    Returns:
        JSONResponse: Response indicating success or failure.
    """
    try:
        new_http_check = models.HttpCheck(
            name=http_check.name,
            uri=http_check.uri,
            is_paused=http_check.is_paused,
            num_retries=http_check.num_retries,
            uptime_sla=http_check.uptime_sla,
            response_time_sla=http_check.response_time_sla,
            use_ssl=http_check.use_ssl,
            response_status_code=http_check.response_status_code,
            check_interval_in_seconds=http_check.check_interval_in_seconds
        )

        db.add(new_http_check)
        db.commit()

        logger.info("Data Created: {}".format(new_http_check.to_dict()))
        return_data = json.loads(
            json.dumps(db.query(models.HttpCheck).filter_by(id=new_http_check.id).first().to_dict(),
                       indent=4, sort_keys=True, default=str))

        crd_data = get_crd_data()

        if crd_data:
            try:
        
                crd = {
                    "apiVersion": crd_data.get("api_version"),
                    "kind": crd_data.get("kind"),
                    "metadata": {
                        "name": str(new_http_check.id),
                    },
                    "spec": {
                        "uri": new_http_check.uri,
                        "checkCreated": str(new_http_check.check_created),
                        "checkIntervalInSeconds": int(new_http_check.check_interval_in_seconds),
                        "checkUpdated": str(new_http_check.check_updated),
                        "id": str(new_http_check.id),
                        "isPaused": new_http_check.is_paused,
                        "name": new_http_check.name,
                        "numRetries": int(new_http_check.num_retries),
                        "responseStatusCode": int(new_http_check.response_status_code),
                        "responseTimeSLA": int(new_http_check.response_time_sla),
                        "uptimeSLA": int(new_http_check.uptime_sla),
                        "useSSL": new_http_check.use_ssl
                    }
                }

                api = client.CustomObjectsApi()

                # Create the Custom Resource
                api.create_namespaced_custom_object(
                    group=crd_data.get("group"),
                    version=crd_data.get("version"),
                    namespace=os.getenv("OPERATOR_NAMESPACE"),
                    plural=crd_data.get("plural"),
                    body=crd
                )
            except Exception as e:
                logger.error(str(e))
        else:
            logger.error("Error while creating CR")

        return response("HTTP Check Created Successfully", status.HTTP_201_CREATED, return_data, log_level="info")
    except Exception as e:
        logger.error(str(e))
        return response(str(e), status.HTTP_400_BAD_REQUEST)


@app.get("/v1/http-check/{id}")
async def get_http_check(id: str, db: Session = Depends(get_db)):
    """Get HTTP Check by ID Endpoint.

    Args:
        id (str): The ID of the HTTP Check.
        db (Session): The database session.

    Returns:
        JSONResponse: Response with HTTP Check data.
    """
    try:
        # Check if http check exists
        http_check = db.query(models.HttpCheck).filter_by(id=id).first()
        if not http_check:
            return response("Http Check not found", status.HTTP_404_NOT_FOUND)

        # Todo: Check if the user who created is asking for the data
        return response("Http Check data retrieved successfully", status.HTTP_200_OK,
                        data=json.loads(json.dumps(http_check.to_dict(), indent=4, sort_keys=True, default=str)),
                        log_level="info")
    except Exception as e:
        return response(str(e), status.HTTP_400_BAD_REQUEST)


# Update HTTP Check
@app.put("/v1/http-check/{id}")
async def update_http_check(id: str, data: HttpCheck, db: Session = Depends(get_db)):
    """Update HTTP Check Endpoint.

    Args:
        id (str): The ID of the HTTP Check.
        data (HttpCheck): The updated data for the HTTP Check.
        db (Session): The database session.

    Returns:
        JSONResponse: Response indicating success or failure.
    """
    try:
        http_check = db.query(models.HttpCheck).filter_by(id=id).first()
        if not http_check:
            return response("Check not found", status.HTTP_404_NOT_FOUND)

        # Update check data
        http_check.name = data.name
        http_check.uri = data.uri
        http_check.is_paused = data.is_paused
        http_check.num_retries = data.num_retries
        http_check.uptime_sla = data.uptime_sla
        http_check.response_time_sla = data.response_time_sla
        http_check.use_ssl = data.use_ssl
        http_check.response_status_code = data.response_status_code
        http_check.check_interval_in_seconds = data.check_interval_in_seconds

        db.add(http_check)
        db.commit()
        db.refresh(http_check)

        crd_data = get_crd_data()

        if crd_data:
            try:
                crd = {
                    "apiVersion": crd_data.get("api_version"),
                    "kind": crd_data.get("kind"),
                    "metadata": {
                        "name": str(http_check.id),
                    },
                    "spec": {
                        "uri": http_check.uri,
                        "checkCreated": str(http_check.check_created),
                        "checkIntervalInSeconds": int(http_check.check_interval_in_seconds),
                        "checkUpdated": str(http_check.check_updated),
                        "id": str(http_check.id),
                        "isPaused": http_check.is_paused,
                        "name": http_check.name,
                        "numRetries": int(http_check.num_retries),
                        "responseStatusCode": int(http_check.response_status_code),
                        "responseTimeSLA": int(http_check.response_time_sla),
                        "uptimeSLA": int(http_check.uptime_sla),
                        "useSSL": http_check.use_ssl
                    }
                }

                # Instantiate CustomObjectsApi
                api = client.CustomObjectsApi()

                # Update the Custom Resource
                api.patch_namespaced_custom_object(
                    group=crd_data.get("group"),
                    version=crd_data.get("version"),
                    namespace=os.getenv("OPERATOR_NAMESPACE"),
                    plural=crd_data.get("plural"),
                    name=str(http_check.id),
                    body=crd
                )
            except Exception as e:
                logger.error(str(e))
        else:
            logger.error("Error while updating CR")

        return response("HTTP Check Updated successfully", status.HTTP_204_NO_CONTENT, log_level="info",
                        no_content=True)
    except Exception as e:
        return response(str(e), status.HTTP_400_BAD_REQUEST)


@app.delete("/v1/http-check/{id}")
async def delete_http_check(id: str, db: Session = Depends(get_db)):
    """Delete HTTP Check Endpoint.

    Args:
        id (str): The ID of the HTTP Check.
        db (Session): The database session.

    Returns:
        JSONResponse: Response indicating success or failure.
    """
    try:
        # Check if HTTP Check exists
        http_check = db.query(models.HttpCheck).filter_by(id=id).first()
        if not http_check:
            return response("HTTP Check not found", status.HTTP_404_NOT_FOUND)

        # Todo: Check if the user who created is deleting the data
        db.delete(http_check)
        db.commit()

        crd_data = get_crd_data()

        if crd_data:
            try:

                api = client.CustomObjectsApi()

                # Delete the Custom Resource
                api.delete_namespaced_custom_object(
                    group=crd_data.get("group"),
                    version=crd_data.get("version"),
                    namespace=os.getenv("OPERATOR_NAMESPACE"),
                    plural=crd_data.get("plural"),
                    name=id
                )
            except Exception as e:
                logger.error(str(e))
        else:
            logger.error("Error while deleting CR")

        return response("HTTP Check deleted successfully", status.HTTP_204_NO_CONTENT, log_level="info",
                        no_content=True)
    except Exception as e:
        return response(str(e), status.HTTP_400_BAD_REQUEST)


# Get All HTTP Checks
@app.get("/v1/http-check")
async def get_http_checks(db: Session = Depends(get_db)):
    """Get All HTTP Checks Endpoint.

    Args:
        db (Session): The database session.

    Returns:
        List[dict]: List of dictionaries containing HTTP Check data.
    """
    try:
        http_checks = db.query(models.HttpCheck).all()

        http_checks_data = [http_check.to_dict() for http_check in http_checks]
        print(http_checks_data)

        logger.info("HTTP Checks fetched successfully 200")
        return http_checks_data

    except Exception as e:
        return response(str(e), status.HTTP_400_BAD_REQUEST)
    