from flask import Blueprint, request, jsonify
from flask_security import auth_required
from backend.services.opensearch_service import OpenSearchService
from backend.services import DoctorService

search_bp = Blueprint("search_bp", __name__, url_prefix="/api/search")

@search_bp.route("/doctors", methods=["GET"])
@auth_required('token', 'session')
def search_doctors():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([]), 200

    # 1. Query OpenSearch
    results = OpenSearchService.search_doctors(query)
    
    # 2. Fallback to standard database search if OpenSearch returns no results (or is down)
    if not results:
        # Search via SQL DB fallback
        db_results = DoctorService.get_all(search=query)
        results = []
        for doc in db_results:
            dept_name = doc.get("department", {}).get("name") if doc.get("department") else "General"
            results.append({
                "id": doc["id"],
                "name": doc.get("user", {}).get("name", "") if doc.get("user") else "",
                "email": doc.get("user", {}).get("email", "") if doc.get("user") else "",
                "specialization": doc["specialization"],
                "qualifications": doc["qualifications"],
                "experience": doc["experience"],
                "department_name": dept_name
            })
            
    return jsonify(results), 200
