from abc import ABC, abstractmethod

from django.conf import settings

import requests

from cvsai.constants import SUPPORTED_LANGUAGES


class BaseTranslationService(ABC):
    """Abstract base class for translation services."""

    @abstractmethod
    def translate(self, text: str, target_language: str, source_language: str = 'en'):
        pass


class GoogleTranslateService(BaseTranslationService):
    """Google Translate API service."""

    def __init__(self):
        self.api_key = getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', None)
        self.base_url = 'https://translation.googleapis.com/language/translate/v2'

    def translate(
        self, text: str, target_language: str, source_language: str = 'en'
    ) -> str:
        if not self.api_key:
            return f"[Translation to {target_language}] {text}"

        try:
            params = {
                'key': self.api_key,
                'q': text,
                'target': target_language,
                'source': source_language,
                'format': 'text',
            }

            response = requests.post(self.base_url, data=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            return result['data']['translations'][0]['translatedText']

        except Exception as exc:
            return f"[Translation error: {str(exc)}] {text}"


class OpenAITranslationService(BaseTranslationService):
    """OpenAI GPT-based translation service."""

    def __init__(self):
        self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
        self.base_url = 'https://api.openai.com/v1/chat/completions'

    def translate(
        self, text: str, target_language: str, source_language: str = 'en'
    ) -> str:
        if not self.api_key:
            return f"[OpenAI Translation to {target_language}] {text}"

        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }

            prompt = (
                f"Translate the following text from {source_language} to {target_language}. "
                f"Return only the translation without any additional text:\n\n{text}"
            )

            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are a professional translator. Translate accurately and maintain formatting.',
                    },
                    {'role': 'user', 'content': prompt},
                ],
                'max_tokens': len(text) * 2,  # Rough estimate
                'temperature': 0.1,  # Low temperature for consistent translations
            }

            response = requests.post(
                self.base_url, json=data, headers=headers, timeout=30
            )
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content'].strip()

        except Exception as exc:
            return f"[OpenAI Translation error: {str(exc)}] {text}"


class MockTranslationService(BaseTranslationService):
    """Mock translation service for testing/demo."""

    def translate(
        self, text: str, target_language: str, source_language: str = 'en'
    ) -> str:
        return f"[MOCK {target_language.upper()}] {text}"


def get_translation_service():
    """Get configured translation service."""
    service_type = getattr(settings, 'TRANSLATION_SERVICE', 'mock')

    if service_type == 'google':
        return GoogleTranslateService()
    if service_type == 'openai':
        return OpenAITranslationService()
    return MockTranslationService()


def translate_cv_content(resume, target_language: str) -> dict:
    """
    Translate CV content to target language.

    Returns dict with translated content.
    """
    service = get_translation_service()

    translated_content = {
        'firstname': resume.firstname,  # Names usually don't translate
        'lastname': resume.lastname,
        'title': service.translate(resume.title, target_language),
        'bio': service.translate(resume.bio, target_language) if resume.bio else '',
        'skills': [],
        'projects': [],
        'contacts': resume.contacts.all(),  # Contacts don't translate
        'language': target_language,
        'language_name': SUPPORTED_LANGUAGES.get(target_language, {}).get(
            'name', target_language
        ),
    }

    # Translate skills (skill names might not translate well)
    for resume_skill in resume.resumeskill_set.all():
        translated_content['skills'].append(
            {
                'name': resume_skill.skill.name,  # Keep original skill name
                'level': service.translate(
                    resume_skill.get_level_display(), target_language
                ),
            }
        )

    # Translate projects
    for project in resume.projects.all():
        translated_content['projects'].append(
            {
                'title': service.translate(project.title, target_language),
                'description': service.translate(project.description, target_language),
                'url': project.url,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'is_ongoing': project.is_ongoing,
            }
        )

    return translated_content
