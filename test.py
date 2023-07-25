from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
class Login:
    
    root=Tk()
    def _init_(self):
     self.root=Login.root
     self.root.title("Login form")
     self.root.geometry("1199x600+100+50")
    #  self.bg=Image.open("images/img2.jpg")
     
     self.bg=ImageTk.PhotoImage(file="images/pexels-photo-673648.jpeg")
     self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
     
     
     Frame_login=Frame(self.root,bg="white")
     Frame_login.place(x=300,y=130,height=345,width=500)
     
     title=Label(Frame_login,text="login here",font=("Times New Roman",25,"bold"),fg="#77337D",bg="white").place(x=90,y=30)
     desc=Label(Frame_login,text="provident fund Login",font=("Times New Roman",15,"bold"),fg="#77337D",bg="white").place(x=90,y=80)
     
     
     lbl_user=Label(Frame_login,text="username",font=("Times New Roman",16,"bold"),fg="gray",bg="white").place(x=90,y=130) 
     self.txt_user=Entry(Frame_login,font=("times new roman",15),bg="lightgray")
     self.txt_user.place(x=90,y=170,width=350,height=35) 
     
     
     lbl_pass=Label(Frame_login,text="password",font=("Times New Roman",16,"bold"),fg="gray",bg="white").place(x=90,y=210) 
     self.txt_pass=Entry(Frame_login,font=("times new roman",15),bg="lightgray")
     self.txt_pass.place(x=90,y=240,width=350,height=35) 
     
     
     forget=Button(Frame_login,text="forget password!!!",bg="white",fg="#D77337",font=("times new roman",12)).place(x=90,y=280)
     login_btn=Button(self.root,command=self.login_function,text="login",bg="#D77337",bd=0,font=("times new roman",12)).place(x=450,y=450,width=180,height=20)
      
    def login_function(self):
         
        if self.txt_pass==""   or self.txt_user.get()=="":
             messagebox.showerror("error","all feild are required",parent=self.root) 
        elif  self.txt_pass.get()!="1234" or self.txt_user.get()!="garima":
             messagebox.showerror("error","invalid username or password",parent=self.root)    
        else:
            messagebox.showinfo("welcome",f"welcome : {self.txt_user.get()}\nyour password:{self.txt_pass.get()}\n",parent=self.root)
            screen=Toplevel(Login.root)
            screen.title("welcome")
            screen.geometry('925x500+300+200')
            screen.config(bg="white")
            Label(screen,text='welcome!!!',bg='#fff',font=('calibri(body)',50,'bold')).pack(expand=True)
 
obj=Login()     
obj.root.mainloop()