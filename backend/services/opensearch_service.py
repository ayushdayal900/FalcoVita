import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

class OpenSearchService:
    INDEX_NAME = "doctors"

    @classmethod
    def get_url(cls):
        try:
            return current_app.config.get("OPENSEARCH_URL", "http://localhost:9200")
        except RuntimeError:
            # Outside flask app context (e.g. celery workers, testing startup, CLI)
            import os
            return os.environ.get("OPENSEARCH_URL", "http://localhost:9200")

    @classmethod
    def init_index(cls):
        url = f"{cls.get_url()}/{cls.INDEX_NAME}"
        try:
            # Check if index exists
            resp = requests.head(url, timeout=1.0)
            if resp.status_code == 200:
                return True
            
            # Create index with mappings
            mapping = {
                "mappings": {
                    "properties": {
                        "name": { "type": "text", "analyzer": "standard" },
                        "email": { "type": "keyword" },
                        "specialization": { "type": "text", "analyzer": "standard" },
                        "qualifications": { "type": "text" },
                        "experience": { "type": "integer" },
                        "department_name": { "type": "text", "analyzer": "standard" }
                    }
                }
            }
            resp = requests.put(url, json=mapping, timeout=1.0)
            if resp.status_code in [200, 201]:
                logger.info(f"OpenSearch index '{cls.INDEX_NAME}' initialized successfully.")
                return True
            else:
                logger.warning(f"Failed to create OpenSearch index: {resp.text}")
        except Exception as e:
            logger.warning(f"Could not connect to OpenSearch to initialize index: {e}")
        return False

    @classmethod
    def index_doctor(cls, doctor):
        cls.init_index() # Ensure index exists
        url = f"{cls.get_url()}/{cls.INDEX_NAME}/_doc/{doctor.id}"
        
        # Safely get department name
        dept_name = doctor.department.name if doctor.department else "General"
        
        doc_data = {
            "name": doctor.user.name if doctor.user else "",
            "email": doctor.user.email if doctor.user else "",
            "specialization": doctor.specialization or "",
            "qualifications": doctor.qualifications or "",
            "experience": doctor.experience or 0,
            "department_name": dept_name
        }
        try:
            resp = requests.put(url, json=doc_data, timeout=1.0)
            if resp.status_code in [200, 201]:
                logger.info(f"Doctor {doctor.id} indexed in OpenSearch.")
                return True
            else:
                logger.warning(f"Failed to index doctor {doctor.id} in OpenSearch: {resp.text}")
        except Exception as e:
            logger.warning(f"Failed to connect to OpenSearch for indexing doctor {doctor.id}: {e}")
        return False

    @classmethod
    def delete_doctor(cls, doctor_id):
        url = f"{cls.get_url()}/{cls.INDEX_NAME}/_doc/{doctor_id}"
        try:
            resp = requests.delete(url, timeout=1.0)
            if resp.status_code == 200:
                logger.info(f"Doctor {doctor_id} deleted from OpenSearch.")
                return True
            elif resp.status_code == 404:
                return True
            else:
                logger.warning(f"Failed to delete doctor {doctor_id} from OpenSearch: {resp.text}")
        except Exception as e:
            logger.warning(f"Failed to connect to OpenSearch to delete doctor {doctor_id}: {e}")
        return False

    @classmethod
    def search_doctors(cls, query_str):
        if not query_str:
            return []
            
        url = f"{cls.get_url()}/{cls.INDEX_NAME}/_search"
        search_query = {
            "query": {
                "multi_match": {
                    "query": query_str,
                    "fields": ["name^2", "specialization^2", "department_name", "qualifications"]
                }
            }
        }
        try:
            resp = requests.post(url, json=search_query, timeout=1.5)
            if resp.status_code == 200:
                hits = resp.json().get("hits", {}).get("hits", [])
                results = []
                for hit in hits:
                    source = hit["_source"]
                    source["id"] = int(hit["_id"])
                    results.append(source)
                return results
            else:
                logger.warning(f"OpenSearch search query failed: {resp.text}")
        except Exception as e:
            logger.warning(f"Could not connect to OpenSearch for search: {e}")
        return []
