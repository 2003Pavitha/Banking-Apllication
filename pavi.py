import mysql.connector
import streamlit as s
s.balloons()

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345',
    database='bank'
)
a=mydb.cursor()
op=['signup','login']
option=s.selectbox('OPTION',op)



if option=='signup':
    cname=s.text_input('NAME')
    phno=s.number_input('phno',min_value=0)
    amount=s.number_input('AMOUNT',min_value=1000)
    pin=s.number_input('CREATE A PIN',min_value=0)
    password=s.text_input('CREATE A PASSWORD',type="password")
    photo=s.file_uploader("UPLOAD YOUR PHOTO",type=['jpg','svg','pdf'])
    submit=s.button('create the account',type='primary')
    if submit:
        query="insert into customer (cname,phno,balance,pin,password,photo) values(%s,%s,%s,%s,%s,%s)"
        val=[cname,phno,amount,pin,password,photo.read()]
        a.execute(query,val)
        mydb.commit()
        s.success('account created sucesfully')

elif option=='login':
    id=s.sidebar.number_input('enter your customer id',min_value=0)
    password=s.sidebar.text_input('enter your password',type='password')
    login=s.sidebar.button('LOGIN',type='primary')
    if 'logged' not in s.session_state:
        s.session_state.logged=False
    if login:
        query = f'SELECT cid, password, balance FROM customer WHERE cid = {id}'
        a.execute(query)
        details = a.fetchall()
        if details:
            if id==details[0][0]:
                if password==details[0][1]:
                    s.sidebar.success('login_sucessfull..')
                    s.session_state.logged=True
                else:
                    s.sidebar.error('password is not matching..')
        else:
            s.sidebar.error('id is not matching..')
    if s.session_state.logged:
        radio = s.radio('choose the option:', ['deposit', 'withdraw', 'balance'])
        if radio == 'deposit':
            pin = s.number_input('enter the pin', min_value=0)
            amt = s.number_input('enter the amount:', min_value=0)
            if s.button('deposit'):
                query = f"select pin from customer where cid={id}"
                a.execute(query)
                d = a.fetchall()
                if pin == d[0][0]:
                    query = f"update customer set balance=balance+{amt} where cid={id}"
                    a.execute(query)
                    mydb.commit()
                    s.success('amount deposited sucesfylly..')
                else:
                    s.error('PIN IS NOT MATCHING...')

        elif radio == 'withdraw':
            pin = s.number_input('enter the pin', min_value=0)
            amt = s.number_input('enter the amount:', min_value=0)
            if s.button('withdraw'):
                query = f"select pin,balance from customer where cid={id}"
                a.execute(query)
                d = a.fetchall()
                if pin == d[0][0]:
                    if d[0][1] > 0:
                        if amt <= d[0][1]:
                            query = f"update customer set balance=balance-{amt} where cid={id}"
                            a.execute(query)
                            mydb.commit()
                            s.success(f'{amt} got debited from your account')
                        else:
                            s.error('INSUFFICIENT BALANCE')
                    else:
                        s.error('ACCOUNT CONTAINS:0RS')
    else:
        pin = s.number_input('enter the pin', min_value=0)
        if s.button('balance_check'):
            query = f"select pin,balance from customer where cid={id}"
            a.execute(query)
            d = a.fetchall()
            if pin == d[0][0]:
                s.success(f'account balance is :{d[0][1]}RS')
            else:
                s.error('pin is not matching..')
