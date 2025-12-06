from backend.models import Department
from backend.extensions import db
from backend.services.service_errors import ServiceError


class DepartmentService:

    # -------------------------------------------
    # GET department by ID
    # -------------------------------------------
    @staticmethod
    def get_by_id(department_id):
        return Department.query.filter_by(id=department_id).first()

    # -------------------------------------------
    # LIST all departments
    # -------------------------------------------
    @staticmethod
    def get_all():
        departments = Department.query.all()
        if not departments:
            raise ServiceError("No departments found")

        return [d.to_dict() for d in departments]

    # -------------------------------------------
    # CREATE department
    # -------------------------------------------
    @staticmethod
    def create(data):
        required = ["name"]
        for field in required:
            if field not in data:
                raise ServiceError(f"Missing required field: {field}")

        # unique constraint check
        if Department.query.filter_by(name=data["name"]).first():
            raise ServiceError("Department with this name already exists")

        new_dept = Department(
            name=data["name"],
            overview=data.get("overview")
        )

        db.session.add(new_dept)
        db.session.commit()
        return new_dept

    # -------------------------------------------
    # UPDATE department
    # -------------------------------------------
    @staticmethod
    def update(data):
        dept = Department.query.filter_by(id=data.get("id")).first()
        if not dept:
            raise ServiceError(f"Department with id {data.get('id')} not found")

        dept.name = data.get("name", dept.name)
        dept.overview = data.get("overview", dept.overview)

        db.session.commit()
        return dept

    # -------------------------------------------
    # DELETE department
    # -------------------------------------------
    @staticmethod
    def delete_by_id(department_id):
        dept = Department.query.filter_by(id=department_id).first()
        if not dept:
            raise ServiceError(f"Department with id {department_id} not found")

        db.session.delete(dept)
        db.session.commit()
        return True
