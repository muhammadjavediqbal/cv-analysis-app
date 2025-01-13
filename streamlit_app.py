import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image

# Set page config
st.set_page_config(page_title="CV Analysis App", layout="wide")

# Center the logo using custom CSS
st.markdown(
    """
    <style>
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display centered logo
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=200)
st.markdown('</div>', unsafe_allow_html=True)



# Job templates dictionary
JOB_TEMPLATES = {
    "AI/ML Engineer": {
        "description": "We are seeking a talented AI/ML Engineer to develop and implement cutting-edge machine learning models. The ideal candidate will have a strong foundation in data science and machine learning technologies.",
        "company_name": "InnovateAI Labs",
        "industry": "Artificial Intelligence",
        "location": "San Francisco, CA",
        "responsibilities": """Design and train machine learning models
Develop scalable AI solutions
Collaborate with data scientists and engineers
Optimize model performance and accuracy
Deploy AI models into production
Keep up with AI/ML advancements""",
        "requirements": """3+ years of experience in AI/ML development
Strong programming skills in Python
Experience with TensorFlow or PyTorch
Knowledge of data preprocessing and feature engineering
Understanding of ML algorithms and statistics
Experience with cloud-based ML services""",
        "preferred_quals": """PhD in AI, ML, or related fields
Experience with NLP or computer vision
Knowledge of reinforcement learning
Open-source contributions""",
        "education": "Master's degree in Computer Science or related field",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "Full Stack Developer": {
        "description": "We are seeking a skilled Full Stack Developer to create end-to-end web solutions. The ideal candidate will excel in both front-end and back-end development, with a strong command of modern frameworks.",
        "company_name": "TechSolutions Inc.",
        "industry": "Software Development",
        "location": "Austin, TX",
        "responsibilities": """Develop scalable web applications
Work on both client-side and server-side components
Collaborate with cross-functional teams
Optimize performance and security
Write clean, maintainable code
Troubleshoot and debug issues""",
        "requirements": """3+ years of experience in full-stack development
Proficiency in JavaScript frameworks (React, Node.js)
Experience with RESTful APIs and databases
Knowledge of HTML5, CSS3, and JavaScript
Version control with Git
Understanding of microservices architecture""",
        "preferred_quals": """Experience with TypeScript
Knowledge of Docker and Kubernetes
Experience with cloud platforms (AWS, Azure)
UI/UX sensibilities""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "MERN Stack Developer": {
        "description": "We are hiring a MERN Stack Developer to build dynamic web applications using the MERN (MongoDB, Express, React, Node.js) technology stack. The ideal candidate will have expertise in developing full-stack solutions.",
        "company_name": "NextGen Web Solutions",
        "industry": "Software Development",
        "location": "New York, NY",
        "responsibilities": """Develop and maintain web applications using the MERN stack
Design and manage database architecture
Collaborate with UI/UX designers and backend teams
Optimize application performance
Implement security best practices
Test and debug applications""",
        "requirements": """2+ years of experience with the MERN stack
Strong proficiency in React and Node.js
Experience with MongoDB and Express.js
Knowledge of JavaScript, HTML5, and CSS3
Version control with Git
Understanding of RESTful APIs""",
        "preferred_quals": """Experience with TypeScript
Knowledge of Redux or Context API
Performance optimization skills
Understanding of CI/CD pipelines""",
        "education": "Bachelor's degree in Computer Science or related field",
        "experience": "2+ years",
        "schedule": "40 hours per week",
    },
    "DevOps Engineer": {
        "description": "We are looking for a talented DevOps Engineer to enhance our development and deployment pipelines. The ideal candidate will have strong expertise in automation and cloud infrastructure management.",
        "company_name": "CloudOps Innovations",
        "industry": "Cloud Computing",
        "location": "Seattle, WA",
        "responsibilities": """Develop and manage CI/CD pipelines
Automate infrastructure provisioning
Monitor and optimize system performance
Manage cloud environments
Ensure infrastructure security
Collaborate with engineering teams""",
        "requirements": """3+ years of experience in DevOps
Proficiency in Docker and Kubernetes
Experience with cloud platforms (AWS, Azure, GCP)
Strong scripting skills (Python, Bash)
Knowledge of infrastructure as code (Terraform, Ansible)
Understanding of system monitoring tools""",
        "preferred_quals": """Experience with multi-cloud environments
Knowledge of ELK stack
Security certifications
Experience with serverless computing""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "Python Developer": {
        "description": "Seeking a Python Developer to build and maintain efficient server-side applications. The ideal candidate will have expertise in Python and experience with APIs and databases.",
        "company_name": "PythonPro Solutions",
        "industry": "Software Development",
        "location": "Chicago, IL",
        "responsibilities": """Develop and maintain backend applications
Design and implement APIs
Work with databases (SQL and NoSQL)
Optimize application performance
Debug and resolve issues
Collaborate with cross-functional teams""",
        "requirements": """3+ years of Python development experience
Proficiency in frameworks like Django or Flask
Experience with RESTful APIs
Knowledge of database systems
Understanding of software testing
Version control with Git""",
        "preferred_quals": """Experience with cloud platforms (AWS, GCP)
Knowledge of async programming
Understanding of DevOps practices
Machine learning experience""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "Frontend Developer": {
        "description": "Looking for a Frontend Developer to create engaging and user-friendly web interfaces. The ideal candidate will have a strong focus on responsive design and user experience.",
        "company_name": "WebUX Innovations",
        "industry": "Software Development",
        "location": "Boston, MA",
        "responsibilities": """Develop and maintain responsive web applications
Implement UI/UX designs
Optimize frontend performance
Write reusable code and libraries
Collaborate with designers and developers
Conduct code reviews and testing""",
        "requirements": """3+ years of frontend development experience
Expertise in React, Vue.js, or Angular
Strong skills in HTML5, CSS3, and JavaScript
Experience with responsive design
Knowledge of frontend testing frameworks
Version control with Git""",
        "preferred_quals": """Experience with TypeScript
Knowledge of state management (Redux, Vuex)
UI/UX design experience
Optimization for accessibility""",
        "education": "Bachelor's degree in Computer Science or equivalent experience",
        "experience": "3+ years",
        "schedule": "40 hours per week",
    },
    "Backend Developer": {
        "description": "We are seeking a Backend Developer to design and maintain server-side logic and architecture. The ideal candidate will have expertise in APIs, databases, and scalable system design.",
        "company_name": "BackendTech Co.",
        "industry": "Software Development",
        "location": "Los Angeles, CA",
        "responsibilities": """Develop and maintain server-side applications
Design and implement APIs
Manage database systems
Optimize application performance
Ensure data security and compliance
Collaborate with frontend and DevOps teams""",
        "requirements": """4+ years of backend development experience
Proficiency in Python, Java, or Node.js
Experience with SQL and NoSQL databases
Knowledge of API design and development
Understanding of microservices architecture
Version control with Git""",
        "preferred_quals": """Experience with Docker and Kubernetes
Knowledge of GraphQL
Understanding of CI/CD pipelines
Experience with cloud platforms""",
        "education": "Bachelor's degree in Computer Science or related field",
        "experience": "4+ years",
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
