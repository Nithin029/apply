import requests
import json
from typing import Dict, Optional, List


class ATSApplicationCreator:
    """
    Create applications across ALL ATS platforms using Knit API
    Dynamically supports any ATS platform added to the configuration
    """
    
    def __init__(self, api_key: str, config_file: str = "ats_config.json"):
        """
        Initialize with API key and load ATS configurations from JSON file
        
        Args:
            api_key: Your Knit API key
            config_file: Path to JSON file containing ATS configurations
        """
        self.api_key = api_key
        self.base_url = "https://api.getknit.dev/v1.0/ats.application.create"
        self.config_file = config_file
        
        # Load ATS configurations from JSON file
        try:
            with open(config_file, 'r') as f:
                self.ats_configs = json.load(f)
            print(f"✓ Loaded configurations for {len(self.ats_configs)} ATS platforms")
        except FileNotFoundError:
            print(f"\n❌ Error: Configuration file '{config_file}' not found!")
            print(f"Please create '{config_file}' manually with your ATS configurations.")
            raise
        except json.JSONDecodeError:
            print(f"\n❌ Error: Invalid JSON in configuration file '{config_file}'")
            raise
    
    def get_candidate_payload(self, 
                            first_name: str,
                            last_name: str,
                            email: str,
                            phone: str,
                            title: str = None,
                            company: str = None,
                            degree: str = None,
                            major: str = None,
                            institute: str = None,
                            currently_pursuing: bool = None,
                            address_line1: str = None,
                            city: str = None,
                            state: str = None,
                            country: str = None,
                            zip_code: str = None,
                            work_address: Dict = None,
                            permanent_address: Dict = None,
                            links: List[Dict] = None) -> Dict:
        """Generate candidate object with provided details"""
        candidate = {
            "firstName": first_name,
            "lastName": last_name,
            "phones": [
                {
                    "type": "PERSONAL",
                    "phoneNumber": phone
                }
            ],
            "emails": [
                {
                    "type": "PERSONAL",
                    "email": email
                }
            ]
        }
        
        # Add optional fields
        if title:
            candidate["title"] = title
        if company:
            candidate["company"] = company
        if links:
            candidate["links"] = links
        
        # Add education if provided
        if degree or major or institute:
            candidate["education"] = [
                {
                    "id": "1",
                    "degree": degree or "bachelors degree",
                    "currentlyPursuing": currently_pursuing if currently_pursuing is not None else True,
                    "major": major or "General",
                    "institute": institute or "University"
                }
            ]
        
        # Add addresses
        if any([address_line1, city, state, country, zip_code]):
            candidate["presentAddress"] = {
                "addressLine1": address_line1 or "",
                "city": city or "",
                "state": state or "",
                "country": country or "",
                "zipCode": zip_code or ""
            }
        
        if work_address:
            candidate["workAddress"] = work_address
        
        if permanent_address:
            candidate["permanentAddress"] = permanent_address
        
        return candidate
    
    def create_application(self, 
                          ats_name: str,
                          job_id: str,
                          initial_stage_id: str,
                          first_name: str,
                          last_name: str,
                          email: str,
                          phone: str,
                          candidate_id: str = None,
                          title: str = None,
                          company: str = None,
                          degree: str = None,
                          major: str = None,
                          institute: str = None,
                          currently_pursuing: bool = None,
                          address_line1: str = None,
                          city: str = None,
                          state: str = None,
                          country: str = None,
                          zip_code: str = None,
                          work_address: Dict = None,
                          permanent_address: Dict = None,
                          links: List[Dict] = None,
                          answers: Optional[List[Dict]] = None,
                          metadata: Optional[Dict] = None,
                          attachment: Optional[Dict] = None,
                          source: str = None) -> Dict:
        """
        Create an application in ANY specified ATS
        
        Args:
            ats_name: Name of ATS from config file
            job_id: The job ID to apply for
            initial_stage_id: The initial stage ID
            first_name: Candidate's first name
            last_name: Candidate's last name
            email: Candidate's email
            phone: Candidate's phone number
            candidate_id: Existing candidate ID (optional)
            title: Job title (optional)
            company: Current company (optional)
            degree: Education degree (optional)
            major: Education major (optional)
            institute: Education institute (optional)
            currently_pursuing: Currently pursuing education (optional)
            address_line1: Address line 1 (optional)
            city: City (optional)
            state: State (optional)
            country: Country (optional)
            zip_code: Zip code (optional)
            work_address: Work address dict (optional)
            permanent_address: Permanent address dict (optional)
            links: List of social/web links (optional)
            answers: List of question answers (optional)
            metadata: Additional metadata (optional)
            attachment: Resume/file attachment (optional)
            source: Application source (optional)
        
        Returns:
            Response dictionary from the API
        """
        
        if ats_name not in self.ats_configs:
            raise ValueError(f"ATS '{ats_name}' not found in configuration. "
                           f"Available: {list(self.ats_configs.keys())}\n"
                           f"Use add_ats_to_config() to add new ATS platforms.")
        
        config = self.ats_configs[ats_name]
        
        # Build payload
        payload = {
            "jobId": job_id,
            "initialStageId": initial_stage_id
        }
        
        # Add candidate ID or candidate object
        if candidate_id:
            payload["candidateId"] = candidate_id
        
        # Add candidate object (required for some ATS or if candidateId not provided)
        if not candidate_id or config.get("requires_candidate_object"):
            candidate = self.get_candidate_payload(
                first_name, last_name, email, phone, title, company,
                degree, major, institute, currently_pursuing,
                address_line1, city, state, country, zip_code,
                work_address, permanent_address, links
            )
            payload["candidate"] = candidate
        
        # Add optional fields
        if answers:
            payload["answers"] = answers
        if metadata:
            payload["metaData"] = json.dumps(metadata) if isinstance(metadata, dict) else metadata
        if attachment:
            payload["attachment"] = attachment
        if source:
            payload["source"] = source
        
        # Build headers
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Knit-Integration-Id": config["integration_id"]
        }
        
        # Make API request
        try:
            print(f"\n🚀 Creating application in {ats_name.upper()}...")
            print(f"   Job ID: {job_id}")
            print(f"   Candidate: {first_name} {last_name} ({email})")
            if config.get("notes"):
                print(f"   ⚠ Note: {config['notes']}")
            
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success") == "true" or result.get("success") == True:
                print(f"✓ Application created successfully!")
                if "data" in result:
                    if result['data'].get('applicationId'):
                        print(f"   Application ID: {result['data'].get('applicationId')}")
                    if result['data'].get('candidateId'):
                        print(f"   Candidate ID: {result['data'].get('candidateId')}")
                    if result['data'].get('jobId'):
                        print(f"   Job ID: {result['data'].get('jobId')}")
            else:
                print(f"⚠ Application creation returned: {result}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error creating application: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    print(f"   Response: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Response: {e.response.text}")
            return {"success": False, "error": str(e)}
    
    def create_application_from_dict(self, ats_name: str, data: Dict) -> Dict:
        """
        Create application using a dictionary of parameters
        
        Args:
            ats_name: Name of the ATS platform
            data: Dictionary containing all application data
        
        Returns:
            Response dictionary from the API
        """
        return self.create_application(
            ats_name=ats_name,
            job_id=data["job_id"],
            initial_stage_id=data["initial_stage_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            candidate_id=data.get("candidate_id"),
            title=data.get("title"),
            company=data.get("company"),
            degree=data.get("degree"),
            major=data.get("major"),
            institute=data.get("institute"),
            currently_pursuing=data.get("currently_pursuing"),
            address_line1=data.get("address_line1"),
            city=data.get("city"),
            state=data.get("state"),
            country=data.get("country"),
            zip_code=data.get("zip_code"),
            work_address=data.get("work_address"),
            permanent_address=data.get("permanent_address"),
            links=data.get("links"),
            answers=data.get("answers"),
            metadata=data.get("metadata"),
            attachment=data.get("attachment"),
            source=data.get("source")
        )
    
    def list_configured_ats(self):
        """List all configured ATS platforms"""
        print("\n📋 Configured ATS Platforms:")
        for ats_name, config in self.ats_configs.items():
            status = "✓" if config["integration_id"] != f"YOUR_{ats_name.upper()}_INTEGRATION_ID" else "⚠"
            print(f"   {status} {ats_name}")
            print(f"      Integration ID: {config['integration_id']}")
            print(f"      Requires Candidate Object: {config.get('requires_candidate_object', False)}")
            if config.get('notes'):
                print(f"      Notes: {config['notes']}")
        print(f"\nTotal: {len(self.ats_configs)} ATS platforms configured")
    
    def bulk_create_applications(self, applications: List[Dict]) -> List[Dict]:
        """
        Create multiple applications across different ATS platforms
        
        Args:
            applications: List of dicts, each containing 'ats_name' and application data
        
        Returns:
            List of response dictionaries
        """
        results = []
        print(f"\n🔄 Creating {len(applications)} applications...")
        
        for idx, app_data in enumerate(applications, 1):
            print(f"\n--- Application {idx}/{len(applications)} ---")
            ats_name = app_data.pop("ats_name")
            result = self.create_application_from_dict(ats_name, app_data)
            results.append({
                "ats_name": ats_name,
                "result": result
            })
        
        return results


# Example usage
# if __name__ == "__main__":
#     # Initialize with your API key
#     API_KEY = "{YOUR_API_KEY}"  # Replace with your actual API key
#
#     try:
#         creator = ATSApplicationCreator(API_KEY)
#
#         # List all configured ATS platforms
#         creator.list_configured_ats()
#
#         # Example 1: Add a new ATS to config
#         # creator.add_ats_to_config(
#         #     ats_name="new_ats_platform",
#         #     integration_id="mg_xxxxxxxxxxxxx",
#         #     requires_candidate_object=True,
#         #     notes="Any special requirements"
#         # )
#
#         # Example 2: Update existing ATS
#         # creator.update_ats_in_config(
#         #     ats_name="workable",
#         #     integration_id="mg_NEW_ID_HERE"
#         # )
#
#         # Example 3: Create application in Workable
#         workable_application = {
#             "job_id": "2CA2D5B257",
#             "initial_stage_id": "applied",
#             "first_name": "Nithin",
#             "last_name": "Sharma",
#             "email": "johndoe@gmail.com",
#             "phone": "9999999999",
#             "title": "Registered Nurse",
#             "company": "Medichire",
#             "degree": "bachelors degree",
#             "major": "nursing",
#             "institute": "Osmania University",
#             "answers": [
#                 {
#                     "multipleChoiceAnswers": ["No"],
#                     "id": "a36ea9",
#                     "type": "YES_NO",
#                     "question": "Are you a veteran?",
#                     "answer": "No"
#                 }
#             ]
#         }
#
#         result = creator.create_application_from_dict("workable", workable_application)
#         print(f"\n📄 Response: {json.dumps(result, indent=2)}")
#
#         # Example 4: Bulk create applications across multiple ATS
#         bulk_applications = [
#             {
#                 "ats_name": "workable",
#                 "job_id": "2CA2D5B257",
#                 "initial_stage_id": "applied",
#                 "first_name": "John",
#                 "last_name": "Doe",
#                 "email": "john1@example.com",
#                 "phone": "1111111111"
#             },
#             {
#                 "ats_name": "bamboohr_ats",
#                 "job_id": "22",
#                 "initial_stage_id": "1",
#                 "first_name": "Jane",
#                 "last_name": "Smith",
#                 "email": "jane@example.com",
#                 "phone": "2222222222",
#                 "city": "Bangalore",
#                 "country": "India"
#             }
#         ]
#
#         # results = creator.bulk_create_applications(bulk_applications)
#
#     except Exception as e:
#         print(f"❌ Error: {str(e)}")