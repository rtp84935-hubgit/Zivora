class student:
    def add_student(self,a,b):
        self.sname=a
        self.rollno=b
        
    

a=input('enter your name:')
b=int(input("enter your roll no:"))
ob=student()
ob.add_student(a,b)
print(ob.sname)