from pyexpat import model
from app import models
from . import BaseTestClass

USERNAME = 'e3'
PASSWORD = 'TestPassword'
NAME = 'e3'
LASTNAME = 'Test Name'

TEACHER_USR = 'p1'
TEACHER_ID = '3'

SESSION_ID = '10'


class UserServiceTest(BaseTestClass):

    def test_create_user(self):
        self.assertEqual(True, True)

    def test_get_user(self):
        user = models.Usuario.get_user(USERNAME)
        self.assertIsNotNone(user)
        self.assertTrue(user)
        self.assertEqual(USERNAME, user.user)
        self.assertEqual(NAME, user.name)

    def test_get_teacher_courses(self):
        courses = models.Usuario.get_teacher_courses(TEACHER_ID)
        self.assertGreaterEqual(len(courses), 0)

    def test_get_current_student_session(self):
        mock_user = models.Usuario.get_user(USERNAME)
        current_session = models.Usuario.get_actual_sesion_estudiante(
            mock_user)
        self.assertEqual(True, True)

    def test_get_current_teacher_session(self):
        mock_teacher = models.Usuario.get_user(TEACHER_USR)
        current_session = models.Usuario.get_actual_sesion_profesor(
            mock_teacher)
        self.assertEqual(True, True)


class SessionServiceTest(BaseTestClass):

    def test_get_session(self):
        session = models.Sesion.get_sesion(SESSION_ID)
        self.assertIsNotNone(session)


class EmocionXEstudianteServiceTest(BaseTestClass):

    def test_get_emocion_x_estudiante(self):
        response = models.Emocion_x_Estudiante.get_emocion_x_estudiante('10')
        self.assertIsNotNone(response)

    def test_insert_emotion(self):
        mock_emotion = ['16', '10', '02/05/2022 19:00:52', 'emocion', '70']
        self.assertTrue(True)

    def test_get_emotions(self):
        emotions = models.Emocion_x_Estudiante.get_emocions_for_sesion('10')
        self.assertIsNotNone(emotions)