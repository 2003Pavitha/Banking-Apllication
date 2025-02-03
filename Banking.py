import mysql.connector
import streamlit as s
s.balloons()
s.color_picker('pick')

from streamlit import radio

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='bank'
)
a=mydb.cursor()
option=['login','signup']
option=s.selectbox('OPTION',option)
if option=='signup':
    cname=s.text_input('NAME')
    phno=s.number_input('phno',min_value=0)
    amount=s.number_input('amount',min_value=1000)
    pin=s.number_input('CREATE A PIN',min_value=0)
    password=s.text_input('CREATE A PASSWORD',type="password")
    photo=s.file_uploader('UPLOAD YOUR PHOTO',type=['jpg','svg' 'pdf'])
    submit=s.button('create the account',type='primary')
    if submit:
        query="insert into customer values(cname,phno,balance,pin,password,photo) values(%s,%s,%S,%s,%S"
        values=[cname,phno,amount,pin,password,photo.read()]
        a.execute(query,values)
        mydb.commit()
        s.success('amount credited successfully')
    elif option=='login':
        id=s.number_input('enter your customer id',min_value=0)
        password=s.text_input('enter your password',type='password')
        login=s.button('LOGIN',type='primary')
        if 'logged' not in s.section_state:
            s.session_state.logged=False
        if login:
            query=f'SELECT cid,password,balance FROM customer WHERE cid={id}'
            a.execute(query)
            details=a.fetchall()
                # [(i,dinga@123)]
            if details:
               if id==details[0][1]:
                    if password == details[0][1]:
                        s.write('login successfully')
                        s.session_state.logged=True
                    else:
                        s.sidebar.error ('password is not matching...')
            else:s.sidebar.error('id is not matching')
        if s.session_state.logged:
            radio=s.radio('choose the option:'['deposit','withdraw','balaance'])
            if radio=='deposit':
                pin=s.number_input('enter the pin',min_value=0)
                amt=s.number_input('enter the amount:',min_value=0)
                if s.button('deposit'):
                    query=f'update customer set balance=balance+{amt}where cid={id}'
                    a.execute(query)
                    mydb.commit()

        elif radio=='withdraw':
            pin = s.number_input('enter the pin', min_value=0)
            amt = s.number_input('enter the amount:', min_value=0)
            if s.button('withdraw'):
                query=f'select pin,balance from customer where cid={id}'
                a.execute(query)
                d=a.fetchall()
                if pin ==d[0][1]:
                    if d[0][1]>0:
                        if amt <=d[0][1]:
                            query="update customer set balance =balance-{amt} where cid={id}"







