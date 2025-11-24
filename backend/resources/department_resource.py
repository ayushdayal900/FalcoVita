from flask import Blueprint, request
from flask_restful import Resource, Api
from backend.models import Department, Doctor
from backend.extensions import db

department_bp = Blueprint("department_bp", __name__, url_prefix="/api/departments")
department_api = Api(department_bp)


class DepartmentListResource(Resource):
    def get(self):
        """Get all departments with doctor count"""
        departments = Department.query.all()
        result = []
        
        for dept in departments:
            dept_data = dept.to_dict()
            dept_data['doctor_count'] = Doctor.query.filter_by(department_id=dept.id).count()
            result.append(dept_data)
        
        return result, 200

    def post(self):
        """Create new department"""
        data = request.get_json()
        
        if not data.get('name'):
            return {"message": "Department name required"}, 400
        
        # Check if exists
        existing = Department.query.filter_by(name=data['name']).first()
        if existing:
            return {"message": "Department already exists"}, 409
        
        dept = Department(
            name=data['name'],
            overview=data.get('overview', '')
        )
        
        db.session.add(dept)
        db.session.commit()
        
        return dept.to_dict(), 201


class DepartmentResource(Resource):
    def get(self, id):
        """Get single department with doctors"""
        dept = Department.query.filter_by(id=id).first()
        if not dept:
            return {"message": "Department not found"}, 404
        
        result = dept.to_dict()
        doctors = Doctor.query.filter_by(department_id=id).all()
        result['doctors'] = [d.to_dict() for d in doctors]
        
        return result, 200

    def put(self, id):
        """Update department"""
        dept = Department.query.filter_by(id=id).first()
        if not dept:
            return {"message": "Department not found"}, 404
        
        data = request.get_json()
        dept.name = data.get('name', dept.name)
        dept.overview = data.get('overview', dept.overview)
        
        db.session.commit()
        return dept.to_dict(), 200

    def delete(self, id):
        """Delete department"""
        dept = Department.query.filter_by(id=id).first()
        if not dept:
            return {"message": "Department not found"}, 404
        
        # Check if has doctors
        doctor_count = Doctor.query.filter_by(department_id=id).count()
        if doctor_count > 0:
            return {"message": f"Cannot delete department with {doctor_count} doctors"}, 400
        
        db.session.delete(dept)
        db.session.commit()
        
        return {"message": "Department deleted successfully"}, 200


# Register routes
department_api.add_resource(DepartmentListResource, "/")
department_api.add_resource(DepartmentResource, "/<int:id>")