import datetime

from django.test import TestCase

from django.utils import timezone
from django.urls import reverse

# Create your tests here.
from polls.models import Question


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # Given: a new question with a pub_date in the future
        time = timezone.now() + datetime.timedelta(days=30)
        question = Question(pub_date=time)

        # When: checking if the question was published recently
        published_recently = question.was_published_recently()

        # Then: published_recently is false
        self.assertFalse(published_recently)

    def test_was_published_recently_with_old_question(self):
        # Given: an old question
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(days=30))
        # When: checking if it was published recently
        recently_published = old_question.was_published_recently()
        # Then: recently_published should be false
        self.assertFalse(recently_published)

    def test_was_published_recently_with_recent_question(self):
        # Given: a recent question
        old_question = Question(pub_date=timezone.now() - datetime.timedelta(hours=1))
        # When: checking if it was published recently
        recently_published = old_question.was_published_recently()
        # Then: recently_published should be true
        self.assertTrue(recently_published)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=question_text, pub_date=time)


def get_string_representation(question):
    return '<Question: %s>' % str(question)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [get_string_representation(question)])

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        old_question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [get_string_representation(old_question)]
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [get_string_representation(question2), get_string_representation(question1)]
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question('Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question('Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.text)
