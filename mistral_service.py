import os
import requests
from typing import Dict, List, Optional
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MistralService:
    """Service for generating AI insights using Mistral LLM"""
    
    def __init__(self):
        self.api_key = os.getenv('MISTRAL_API_KEY')
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-medium"
    
    def generate_country_insights(self, analysis_data: Dict) -> Optional[str]:
        """Generate comprehensive insights about country comparison"""
        if not self.is_available():
            return None
            
        try:
            prompt = self._create_analysis_prompt(analysis_data)
            response = self._call_mistral_api(prompt)
            return response
            
        except Exception as e:
            st.warning(f"Error generating AI insights: {str(e)}")
            return None
    
    def extract_key_findings(self, analysis_data: Dict) -> List[str]:
        """Extract key findings from the data"""
        if not self.is_available():
            return []
            
        try:
            prompt = self._create_findings_prompt(analysis_data)
            response = self._call_mistral_api(prompt)
            
            if response:
                # Split response into bullet points
                findings = [line.strip() for line in response.split('\n') if line.strip() and line.strip().startswith('•')]
                return findings[:5]  # Return top 5 findings
            
            return []
            
        except Exception:
            return []
    
    def _create_analysis_prompt(self, analysis_data: Dict) -> str:
        """Create a comprehensive analysis prompt for the LLM"""
        entities = analysis_data.get('entities', [])
        metrics = analysis_data.get('metrics', [])
        data = analysis_data.get('data', {})
        analysis_level = analysis_data.get('analysis_level', 'Country Level')
        
        prompt = f"""
        As an expert data analyst, provide comprehensive insights for this {analysis_level} comparison:
        
        Entities analyzed: {', '.join(entities)}
        Metrics: {', '.join(metrics)}
        
        Data summary:
        """
        
        for entity in entities:
            if entity in data:
                prompt += f"\n{entity}:"
                for metric in metrics:
                    value = data[entity].get(metric)
                    if value is not None:
                        prompt += f"\n  - {metric}: {value}"
        
        prompt += """
        
        Please provide:
        1. Key performance patterns and trends
        2. Top and bottom performers with explanations
        3. Strategic recommendations for improvement
        4. Policy implications and next steps
        5. Comparative advantages and challenges
        
        Keep the analysis practical and actionable.
        """
        
        return prompt
    
    def _create_findings_prompt(self, analysis_data: Dict) -> str:
        """Create a prompt specifically for extracting key findings"""
        prompt = self._create_analysis_prompt(analysis_data)
        prompt += "\n\nPlease summarize the top 5 key findings as bullet points starting with '•'."
        return prompt
    
    def _call_mistral_api(self, prompt: str) -> Optional[str]:
        """Make API call to Mistral"""
        if not self.api_key:
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            st.warning(f"Mistral API error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        """Check if the Mistral service is available"""
        return bool(self.api_key)
    
    def get_service_status(self) -> str:
        """Get current service status"""
        if self.is_available():
            return "✅ Mistral AI Connected"
        else:
            return "🔑 Add MISTRAL_API_KEY to .env file"