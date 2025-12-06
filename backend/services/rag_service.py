import os
try:
    from pinecone import Pinecone
except ImportError:
    Pinecone = None
from backend.models import Doctor, Department, Appointment

class RAGService:
    @staticmethod
    def retrieve_context(query, role, user_id=None):
        """
        Real RAG retrieval using Pinecone.
        """
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
             # Fallback to SQL mock
            return RAGService._mock_retrieve_context(query, role, user_id)

        try:
            pc = Pinecone(api_key=api_key)
            index_name = "falcovita-rag" # Assuming this index exists
            
            # Check if index exists, if not, fallback
            if index_name not in [i.name for i in pc.list_indexes()]:
                 return RAGService._mock_retrieve_context(query, role, user_id)

            index = pc.Index(index_name)

            # Generate embedding for query (using OpenAI)
            import openai
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            
            embedding_response = openai.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            vector = embedding_response.data[0].embedding

            # Query Pinecone
            results = index.query(
                vector=vector,
                top_k=3,
                include_metadata=True
            )

            context = "Retrieved Information:\n"
            for match in results['matches']:
                context += f"- {match['metadata']['text']}\n"
            
            return context

        except Exception as e:
            print(f"RAG Error: {e}")
            return RAGService._mock_retrieve_context(query, role, user_id)

    @staticmethod
    def _mock_retrieve_context(query, role, user_id=None):
        """
        Fallback SQL-based retrieval
        """
        context = ""
        query_lower = query.lower()
import os
try:
    from pinecone import Pinecone
except ImportError:
    Pinecone = None
from backend.models import Doctor, Department, Appointment, Patient

class RAGService:
    @staticmethod
    def retrieve_context(query, role, user_id=None):
        """
        Real RAG retrieval using Pinecone.
        """
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
             # Fallback to SQL mock
            return RAGService._mock_retrieve_context(query, role, user_id)

        try:
            pc = Pinecone(api_key=api_key)
            index_name = "falcovita-rag" # Assuming this index exists
            
            # Check if index exists, if not, fallback
            if index_name not in [i.name for i in pc.list_indexes()]:
                 return RAGService._mock_retrieve_context(query, role, user_id)

            index = pc.Index(index_name)

            # Generate embedding for query (using OpenAI)
            import openai
            openai.api_key = os.environ.get("OPENAI_API_KEY")
            
            embedding_response = openai.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            vector = embedding_response.data[0].embedding

            # Query Pinecone
            results = index.query(
                vector=vector,
                top_k=3,
                include_metadata=True
            )

            context = "Retrieved Information:\n"
            for match in results['matches']:
                context += f"- {match['metadata']['text']}\n"
            
            return context

        except Exception as e:
            print(f"RAG Error: {e}")
            return RAGService._mock_retrieve_context(query, role, user_id)

    @staticmethod
    def _mock_retrieve_context(query, role, user_id=None):
        """
        Fallback SQL-based retrieval
        """
        context = ""
        query_lower = query.lower()

        if role == 'admin':
            if "appointment" in query_lower:
                count = Appointment.query.count()
                context += f"Total appointments in system: {count}. "
            if "doctor" in query_lower:
                doctors = Doctor.query.all()
                count = len(doctors)
                names = ", ".join([d.user.name for d in doctors if d.user])
                context += f"Total doctors: {count}. Names: {names}. "
            if "patient" in query_lower:
                patients = Patient.query.limit(10).all()
                names = ", ".join([p.user.name for p in patients if p.user])
                context += f"Total patients: {Patient.query.count()}. recent patients: {names}. "

        elif role == 'patient':
            if "cardiologist" in query_lower:
                cardio = Department.query.filter(Department.name.ilike('%cardio%')).first()
                if cardio:
                    doctors = Doctor.query.filter_by(department_id=cardio.id).all()
                    doc_names = [d.user.name for d in doctors if d.user]
                    context += f"Available Cardiologists: {', '.join(doc_names)}. "
            if "doctor" in query_lower:
                 # General doctor search for patients
                doctors = Doctor.query.limit(5).all()
                doc_names = [d.user.name for d in doctors if d.user]
                context += f"Some of our doctors: {', '.join(doc_names)}. "

        return context
