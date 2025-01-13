import streamlit as st
import requests
import json
import pandas as pd

# Set page config
st.set_page_config(page_title="CV Analysis App", layout="wide")

# Job templates dictionary
JOB_TEMPLATES = {
    "Senior Full Stack Developer": {
        "description": "We are seeking an experienced Full Stack Developer to join our dynamic team. The ideal candidate will have a strong background in both front-end and back-end development, with expertise in modern web technologies.",
        "company_name": "TechCorp Solutions",
        "industry": "Information Technology",
        "location": "San Francisco, CA",
        "responsibilities": """Design and implement scalable web applications
Lead technical architecture decisions
Mentor junior developers
Collaborate with cross-functional teams
Optimize application performance
Implement security best practices""",
        "requirements": """5+ years of experience in full-stack development
Strong proficiency in React, Node.js, and Python
Experience with cloud services (AWS/Azure)
Strong understanding of database design
Experience with microservices architecture
Excellent problem-solving skills""",
        "preferred_quals": """Experience with Kubernetes
Knowledge of DevOps practices
Machine learning experience
Open source contributions""",
        "education": "Bachelor's degree in Computer Science or related field",
        "experience": "5+ years",
        "schedule": "40 hours per week",
    },
    "Frontend Developer": {
        "description": "Looking for a talented Frontend Developer to create responsive and user-friendly web interfaces. The ideal candidate will have strong UI/UX sensibilities and expertise in modern frontend frameworks.",
        "company_name": "WebFront Innovations",
        "industry": "Software Development",
        "location": "New York, NY",
        "responsibilities": """Develop responsive web applications
Implement UI/UX designs
Optimize frontend performance
Write clean, maintainable code
Collaborate with designers
Conduct code reviews""",
        "requirements": """3+ years of frontend development experience
Expertise in React or Vue.js
Strong HTML5, CSS3, and JavaScript skills
Experience with responsive design
Knowledge of frontend testing frameworks
Version control with Git""",
        "preferred_quals": """Experience with TypeScript
Knowledge of Redux or Vuex
UI/UX design experience
Performance optimization skills""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "Backend Developer": {
        "description": "Seeking a skilled Backend Developer to build and maintain server-side applications. The ideal candidate will have strong expertise in API development and database management.",
        "company_name": "ServerSide Tech",
        "industry": "Software Development",
        "location": "Austin, TX",
        "responsibilities": """Design and implement RESTful APIs
Manage database architecture
Optimize server performance
Implement security measures
Write automated tests
Handle system integration""",
        "requirements": """4+ years of backend development experience
Strong Python or Node.js expertise
Experience with SQL and NoSQL databases
Knowledge of API design principles
Understanding of cloud services
Experience with microservices""",
        "preferred_quals": """Experience with Docker
Knowledge of message queues
Familiarity with GraphQL
Security certification""",
        "education": "Bachelor's degree in Computer Science or related field",
        "experience": "4+ years",
        "schedule": "40 hours per week",
    },
    "DevOps Engineer": {
        "description": "Looking for a DevOps Engineer to streamline our development and deployment processes. The ideal candidate will have strong automation and infrastructure management skills.",
        "company_name": "CloudOps Solutions",
        "industry": "Cloud Computing",
        "location": "Seattle, WA",
        "responsibilities": """Manage CI/CD pipelines
Implement infrastructure as code
Monitor system performance
Automate deployment processes
Manage cloud infrastructure
Implement security measures""",
        "requirements": """3+ years of DevOps experience
Strong Linux/Unix administration skills
Experience with AWS or Azure
Expertise in Docker and Kubernetes
Knowledge of Python or Shell scripting
Experience with monitoring tools""",
        "preferred_quals": """Security certifications
Experience with Terraform
Knowledge of ELK stack
Multi-cloud experience""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    }
}


# Initialize session state for storing all data
if 'app_state' not in st.session_state:
    st.session_state.app_state = {
        'cv_data': None,
        'cv_processed': False,
        'relevancy_data': None,
        'relevancy_checked': False,
        'improved_cv': None,
        'cv_improved': False,
        'job_analysis': None,
        'job_submitted': False,
        'assessment_data': None,
        'assessment_generated': False,
        'solution_results': None,
        'solution_submitted': False
    }

def main():
    st.title("CV Analysis Application")
    
    # File upload section
    st.header("1. Upload CV")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file:
        if st.button("Process CV"):
            with st.spinner('Processing CV... Please wait'):
                files = {"file": uploaded_file}
                response = requests.post("https://jinnaylst-cv-module-542808340038.us-central1.run.app/convert-cv-to-json/", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        st.session_state.app_state['cv_data'] = result["data"]
                        st.session_state.app_state['cv_processed'] = True
                        st.success("CV processed successfully!")
                    else:
                        st.error(f"Error: {result['message']}")

    # Check CV Relevancy section
    st.header("2. Check CV Relevancy")
    check_relevancy = st.button("Check Relevancy", 
                               disabled=not st.session_state.app_state['cv_processed'])
    
    if check_relevancy:
        with st.spinner('Analyzing CV relevancy... Please wait'):
            response = requests.post(
                "https://jinnaylst-cv-module-542808340038.us-central1.run.app/check_cv_relevancy/",
                json=st.session_state.app_state['cv_data']
            )
            
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    st.session_state.app_state['relevancy_data'] = result["data"]
                    st.session_state.app_state['relevancy_checked'] = True

    # Display relevancy results if available
    if st.session_state.app_state['relevancy_checked']:
        st.subheader("Relevancy Analysis")
        scores_data = st.session_state.app_state['relevancy_data']["score_and_recommendation_for_each_guideline"]
        df = pd.DataFrame(scores_data)
        st.table(df)
        
        st.subheader("Overall Assessment")
        st.write(f"Score: {st.session_state.app_state['relevancy_data']['overall_assessment_score']}/100")
        st.write("Recommendation:", st.session_state.app_state['relevancy_data']['recommendation'])

    # Improve CV section
    improve_cv = st.button("Improve CV", 
                          disabled=not st.session_state.app_state['relevancy_checked'])
    
    if improve_cv:
        with st.spinner('Generating CV improvements... Please wait'):
            improvements_response = requests.post(
                "https://jinnaylst-cv-module-542808340038.us-central1.run.app/improved_cv/",
                json={
                    "cv_data": st.session_state.app_state['cv_data'],
                    "improvements": {
                        "evaluations": st.session_state.app_state['relevancy_data']["score_and_recommendation_for_each_guideline"]
                    }
                }
            )
            
            if improvements_response.status_code == 200:
                improvements_result = improvements_response.json()
                if improvements_result["status"] == "success":
                    st.session_state.app_state['improved_cv'] = improvements_result["data"]
                    st.session_state.app_state['cv_improved'] = True

    # Display improved CV if available
    if st.session_state.app_state['cv_improved']:
        st.success("CV improvements generated successfully!")
        # st.subheader("Improved CV")
        improved_cv = st.session_state.app_state['improved_cv']
        
        # with st.expander("View Improved CV", expanded=True):
        #     # Personal Information
        #     st.write("### Personal Information")
        #     st.write(f"Name: {improved_cv['name']}")
        #     st.write(f"Email: {improved_cv['contact_information']['work_email']}")
            
        #     # Work Experience
        #     st.write("### Work Experience")
        #     for exp in improved_cv['work_experience']:
        #         st.write(f"**{exp['title']} at {exp['company']}**")
        #         st.write(f"{exp['start_date']} - {exp['end_date']}")
        #         st.write(f"Location: {exp['location']}")
        #         if exp.get('responsibilities'):
        #             st.write("Responsibilities:")
        #             for resp in exp['responsibilities']:
        #                 st.write(f"- {resp}")
        #         st.write("---")
            
        #     # Education
        #     st.write("### Education")
        #     for edu in improved_cv['education']:
        #         st.write(f"**{edu['degree']} in {edu['field_of_study']}**")
        #         st.write(f"{edu['institution']}, {edu['location']}")
        #         st.write(f"{edu['start_date']} - {edu['end_date']}")
        #         if edu.get('thesis'):
        #             st.write(f"Thesis: {edu['thesis']}")
        #         st.write("---")
            
        #     # Skills
        #     st.write("### Skills")
        #     st.write(", ".join(improved_cv['skills']))

    # Job Description section
    st.header("3. Submit Job Description")
    with st.expander("Enter Job Description", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            # Add dropdown for job titles
            selected_job = st.selectbox(
                "Select Job Title",
                ["Select a job title..."] + list(JOB_TEMPLATES.keys())
            )
            
            # Auto-fill fields based on selection
            if selected_job != "Select a job title...":
                job_data = JOB_TEMPLATES[selected_job]
                job_description = st.text_area("Job Description", value=job_data["description"], key="job_desc")
                company_name = st.text_input("Company Name", value=job_data["company_name"], key="company_name")
                industry = st.text_input("Industry", value=job_data["industry"], key="industry")
                location = st.text_input("Location", value=job_data["location"], key="location")
            else:
                job_description = st.text_area("Job Description", key="job_desc")
                company_name = st.text_input("Company Name", key="company_name")
                industry = st.text_input("Industry", key="industry")
                location = st.text_input("Location", key="location")
                
        with col2:
            if selected_job != "Select a job title...":
                responsibilities = st.text_area("Key Responsibilities (one per line)", value=job_data["responsibilities"], key="resp")
                requirements = st.text_area("Requirements (one per line)", value=job_data["requirements"], key="req")
                preferred_quals = st.text_area("Preferred Qualifications (one per line)", value=job_data["preferred_quals"], key="preferred")
                education_level = st.text_input("Required Education Level", value=job_data["education"], key="education")
                experience_level = st.text_input("Required Experience Level", value=job_data["experience"], key="experience")
            else:
                responsibilities = st.text_area("Key Responsibilities (one per line)", key="resp")
                requirements = st.text_area("Requirements (one per line)", key="req")
                preferred_quals = st.text_area("Preferred Qualifications (one per line)", key="preferred")
                education_level = st.text_input("Required Education Level", key="education")
                experience_level = st.text_input("Required Experience Level", key="experience")
            
        col3, col4 = st.columns(2)
        with col3:
            job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Temporary", "Internship"])
            if selected_job != "Select a job title...":
                work_schedule = st.text_input("Work Schedule", value=job_data["schedule"], key="schedule")
            else:
                work_schedule = st.text_input("Work Schedule", key="schedule")
        with col4:
            remote_option = st.checkbox("Remote Work Available")
            diversity_initiative = st.checkbox("Part of Diversity Initiative")
        
        submit_job = st.button("Submit Job and CV", 
                              disabled=not st.session_state.app_state['cv_processed'])
        
        if submit_job and all([selected_job != "Select a job title...", job_description, responsibilities, requirements]):
            with st.spinner('Analyzing job match... Please wait'):
                job_data = {
                    "job_title": selected_job,
                    "job_description": job_description,
                    "key_responsibilities": [{"responsibility": r.strip()} for r in responsibilities.split('\n') if r.strip()],
                    "requirements": [r.strip() for r in requirements.split('\n') if r.strip()],
                    "preferred_qualifications": [q.strip() for q in preferred_quals.split('\n') if q.strip()],
                    "deliverables": [],
                    "project_timeline": "Not specified",
                    "next_steps": [],
                    "skills_required": [],
                    "education_level": education_level,
                    "certifications": [],
                    "experience_level": experience_level,
                    "location": location,
                    "company_name": company_name,
                    "job_type": job_type,
                    "industry": industry,
                    "work_schedule": work_schedule,
                    "remote_option": remote_option,
                    "diversity_initiative": diversity_initiative
                }
                
                response = requests.post(
                    "https://jinnaylst-cv-module-542808340038.us-central1.run.app/submit-job-and-cv/",
                    json={
                        "job_description": job_data,
                        "cv": st.session_state.app_state['cv_data']
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        st.session_state.app_state['job_analysis'] = result["data"]
                        st.session_state.app_state['job_submitted'] = True

    # Display job analysis results if available
    if st.session_state.app_state['job_submitted']:
        st.success("Job and CV analysis completed!")
        st.subheader("Analysis Results")
        results_data = {
            "Metric": ["Validity", "Score", "Improvements"],
            "Value": [
                st.session_state.app_state['job_analysis']["validity"],
                st.session_state.app_state['job_analysis']["score"],
                st.session_state.app_state['job_analysis']["improvements"]
            ]
        }
        df = pd.DataFrame(results_data)
        st.table(df)

    # Assessment Test section
    st.header("4. Get Assessment Test")
    generate_assessment = st.button("Generate Assessment", 
                                  disabled=not st.session_state.app_state['cv_processed'])
    
    if generate_assessment:
        with st.spinner('Generating assessment test... Please wait'):
            response = requests.post(
                "https://jinnaylst-cv-module-542808340038.us-central1.run.app/assign_assessment_test/",
                json=st.session_state.app_state['cv_data']
            )
            
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    st.session_state.app_state['assessment_data'] = result["data"]
                    st.session_state.app_state['assessment_generated'] = True

    # Display assessment test if available
    if st.session_state.app_state['assessment_generated']:
        st.success("Assessment test generated successfully!")
        st.subheader("Assessment Test")
        
        with st.expander("View Assessment Details", expanded=True):
            test_data = {
                "Parameter": ["Time Limit", "Problem Statement", "Example Input", "Example Output", "Language"],
                "Details": [
                    st.session_state.app_state['assessment_data']["time_limit"],
                    st.session_state.app_state['assessment_data']["problem_statement"],
                    str(st.session_state.app_state['assessment_data']["example_input"]),
                    str(st.session_state.app_state['assessment_data']["example_output"]),
                    st.session_state.app_state['assessment_data']["language"]
                ]
            }
            df = pd.DataFrame(test_data)
            st.table(df)
            
            st.write("**Evaluation Criteria:**")
            for criterion in st.session_state.app_state['assessment_data']["criteria"]:
                st.write(f"- {criterion}")

        # Solution submission
        st.subheader("Submit Solution")
        solution = st.text_area("Enter your solution here", key="solution_input")
        submit_solution = st.button("Submit Solution", key="submit_solution")
        
        if submit_solution and solution.strip():
            with st.spinner('Evaluating solution... Please wait'):
                
                data_json={
                        "test": st.session_state.app_state['assessment_data'],
                        "solution": {"code": solution}
                    }
                # st.write(f"{data_json}")
                scoring_response = requests.post(
                    "https://jinnaylst-cv-module-542808340038.us-central1.run.app/scoring_assessment_test/",
                    # json={
                    #     "test": st.session_state.app_state['assessment_data'],
                    #     "solution": {"code": solution}
                    # }
                    json=data_json
                )
                
                if scoring_response.status_code == 200:
                    scoring_result = scoring_response.json()
                    if scoring_result["status"] == "success":
                        st.session_state.app_state['solution_results'] = scoring_result["data"]
                        st.session_state.app_state['solution_submitted'] = True
                    else:
                        st.error(f"Error in scoring: {scoring_result.get('message', 'Unknown error')}")
                else:
                    st.error(f"API call failed with status code {scoring_response.status_code}.")

    # Display solution results if available
    if st.session_state.app_state['solution_submitted']:
        st.success("Solution evaluated successfully!")
        
        with st.expander("View Assessment Results", expanded=True):
            scores_data = {
                "Criteria": ["Correctness", "Code Quality", "Logic and Approach", "Error Handling", "Optimization"],
                "Score": [
                    f"{st.session_state.app_state['solution_results']['correctness_score']}/10",
                    f"{st.session_state.app_state['solution_results']['code_quality_score']}/10",
                    f"{st.session_state.app_state['solution_results']['logic_and_approach_score']}/10",
                    f"{st.session_state.app_state['solution_results']['error_handling_score']}/10",
                    f"{st.session_state.app_state['solution_results']['optimization_score']}/10"
                ],
                "Evaluation": [
                    st.session_state.app_state['solution_results']['correctness'],
                    st.session_state.app_state['solution_results']['code_quality'],
                    st.session_state.app_state['solution_results']['logic_and_approach'],
                    st.session_state.app_state['solution_results']['error_handling'],
                    st.session_state.app_state['solution_results']['optimization']
                ]
            }
            # Convert to DataFrame and ensure type consistency
            df = pd.DataFrame(scores_data).astype(str)
            
            st.subheader("Assessment Results")
            st.table(df)
            
            st.subheader("Overall Assessment")
            st.write(f"Total Score: {st.session_state.app_state['solution_results']['overall_assessment']}/10")
            st.write("**Recommendations:**")
            st.write(st.session_state.app_state['solution_results']['recommendation'])

if __name__ == "__main__":
    main()
