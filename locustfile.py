from locust import HttpLocust, HttpUser, task,between

from app.constants import IMAGEN
class HelloWorldUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(900,1000)
    @task(1)
    def get_courses(self):
        self.client.get("/courses")
        # self.client.post("/logout")
    @task(2)
    def get_session(self):
        self.client.get("/info_sesion?id=10",json={"id":10})

    @task(4)   
    def get_courses(self):
        self.client.get("/courses?user=p1&id=3")
 
    # @task(5)
    # def send_image(self):
    #     self.client.post("/login",json={"user":"e1","password":"123"})
    #     self.client.post("/recibir-imagen",json={"image" :IMAGEN,"fecha":"12/10/2021, 15:13:10"})
    #     self.client.post("/logout")
        
    
    def on_start(self):
        self.client.post("/login",json={"user":"p1","password":"123"})
        # self.client.post("/login",json={"user":"e1","password":"123"})
    def on_stop(self):
        self.client.post("/logout")

        
        
    