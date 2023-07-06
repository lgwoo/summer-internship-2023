import random
import sqlite3
import pandas as pd
import tkinter as tk

from datetime import datetime

# SQLite 데이터베이스 연결
#conn = sqlite3.connect('./test.db',isolation_level=None)
conn = sqlite3.connect('//DESKTOP-39REBTR/Users/user/Desktop/2023인턴십/pyworkspace/test.db',isolation_level=None)
cur = conn.cursor()

# TEST 테이블 생성 (계좌 정보 저장)
cur.execute("CREATE TABLE IF NOT EXISTS 'TEST'(account integer ,name text, birth integer, balance integer, passwd text)")
cur.execute("CREATE TABLE IF NOT EXISTS 'HISTORY'(account integer ,date text, type text, amount integer, counterinfo text)")

# BASE 64
def encoding(str: str):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"  #Base64 뱐환 표
    a = ""
    ans = ""
    for i in str:
        a +=(format(ord(i),'08b'))   #입력받은 각 문자를 2진수 바꾸어서 연결
    if len(a)%6!=0:     # 6비트로 나누어 떨어지지 않으면 뒤에 0을 더 넣어줌
        a += "0" * (6-len(a)%6)
    for i in range(0,len(a),6):  # 6자리씩 10진수로 바꿔서 표에 맞게 연결
        ans += base64_chars[int(a[i:i+6],2)]
    return ans
def decoding(str: str):
    pass


# 계좌개설 함수
def adduser():
    def submit():
        name = name_entry.get()
        birth = int(birth_entry.get())

        randnum = random.randint(10000000000, 99999999999)
        cur.execute("SELECT * FROM TEST WHERE account = ?", (randnum,))
        row = cur.fetchone()
        while(row):
            randnum = random.randint(10000000000, 99999999999)
            cur.execute("SELECT * FROM TEST WHERE account = ?", (randnum,))
            row = cur.fetchone()

        encodingpw = encoding(pw_entry.get())
        cur.execute("INSERT INTO TEST VALUES(?,?,?,?,?)", (randnum, name, birth, 0, encodingpw))
        account_label.config(text="계좌번호: " + str(randnum))
        message_label.config(text="계좌가 개설되었습니다. 계좌번호를 꼭 기억해 주세요.")
        confirm_button.pack()
        submit_button.pack_forget()

    
    usertk = tk.Tk()

    name_label = tk.Label(usertk, text="성함을 입력해 주세요")
    name_label.pack()

    name_entry = tk.Entry(usertk)
    name_entry.pack()

    birth_label = tk.Label(usertk, text="생년월일을 입력해 주세요 ex)20030811")
    birth_label.pack()

    birth_entry = tk.Entry(usertk)
    birth_entry.pack()
    
    pw_label = tk.Label(usertk, text="비밀번호를 입력해 주세요.")
    pw_label.pack()

    pw_entry = tk.Entry(usertk, show="*")
    pw_entry.pack()

    submit_button = tk.Button(usertk, text="계좌 개설", command=submit)
    submit_button.pack()

    account_label = tk.Label(usertk, text="")
    account_label.pack()

    message_label = tk.Label(usertk, text="")
    message_label.pack()
    
    def confirm():
        usertk.destroy()

    confirm_button = tk.Button(usertk, text="확인", command=confirm)
    
    usertk.mainloop()


# 입금 함수
def putmoney():
    def submit():
        account_num = int(account_entry.get())
        cur.execute("SELECT * FROM TEST WHERE account = ?", (account_num,))
        row = cur.fetchone()
        if row:
            recipient_name = row[1]
            amount = int(amount_entry.get())
            if amount<=0:
                confirmation_label.config(text="0보다 큰 금액을 입력해 주세요")
                return
            confirmation_label.config(text=f"{recipient_name}님에게 {amount}원을 보내시겠습니까?")
            def confirm():
                cur.execute("UPDATE TEST SET balance = balance + ? WHERE account=?", (amount, account_num))
                cur.execute("INSERT INTO HISTORY VALUES(?,?,?,?,?)", (row[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "입금", amount, "none"))
                inputtk.destroy()

            confirm_button = tk.Button(inputtk, text="확인", command=confirm)
            confirm_button.pack()
            submit_button.pack_forget()
        else:
            confirmation_label.config(text="잘못된 계좌번호 입니다.")

    inputtk = tk.Tk()

    account_label = tk.Label(inputtk, text="카드/통장을 삽입해 주세요 (계좌번호를 입력해 주세요)")
    account_label.pack()

    account_entry = tk.Entry(inputtk)
    account_entry.pack()

    confirmation_label = tk.Label(inputtk, text="")
    confirmation_label.pack()

    amount_label = tk.Label(inputtk, text="얼마를 보내시겠습니까?")
    amount_label.pack()

    amount_entry = tk.Entry(inputtk)
    amount_entry.pack()

    submit_button = tk.Button(inputtk, text="입금", command=submit)
    submit_button.pack()


# 출금 함수
def withdraw():
    def submit():
        account_num = int(account_entry.get())
        cur.execute("SELECT * FROM TEST WHERE account = ?", (account_num,))
        row = cur.fetchone()

        if row:
            password = password_entry.get()
            enpw = encoding(password)
            if row[4] != enpw:
                result_label.config(text="비밀번호가 틀렸습니다.")
            else:
                amount = int(amount_entry.get())
                current_balance = row[3]
                result_label.config(text=f"{row[3]}원이 있습니다.")
                if amount > current_balance:
                    confirmation_label.config(text="계좌의 잔액보다 더 큰 금액을 입력했습니다.")
                elif amount<=0:
                    confirmation_label.config(text="0보다 큰 금액을 입력해 주세요")
                else:
                    confirmation_label.config(text=f"{row[1]}님의 계좌에서 {amount}원을 출금하시겠습니까?")
                    def confirm():
                        cur.execute("UPDATE TEST SET balance = balance - ? WHERE account = ?", (amount, account_num))
                        cur.execute("INSERT INTO HISTORY VALUES (?, ?, ?, ?, ?)", (row[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "출금", amount, "none"))
                        conn.commit()
                        result_label.config(text=f"{amount}원이 출금되었습니다.")
                        withdrawtk.destroy()
                    confirm_button = tk.Button(withdrawtk, text="확인", command=confirm)
                    confirm_button.pack()
                    submit_button.pack_forget()
        else:
            confirmation_label.config(text="잘못된 계좌번호 입니다.")

    withdrawtk = tk.Tk()

    account_label = tk.Label(withdrawtk, text="카드/통장을 삽입해 주세요 (계좌번호를 입력해 주세요)")
    account_label.pack()

    account_entry = tk.Entry(withdrawtk)
    account_entry.pack()

    confirmation_label = tk.Label(withdrawtk, text="")
    confirmation_label.pack()

    password_label = tk.Label(withdrawtk, text="비밀번호를 입력해 주세요.")
    password_label.pack()

    password_entry = tk.Entry(withdrawtk, show="*")
    password_entry.pack()

    amount_label = tk.Label(withdrawtk, text="얼마를 출금하시겠습니까?")
    amount_label.pack()

    amount_entry = tk.Entry(withdrawtk,)
    amount_entry.pack()

    submit_button = tk.Button(withdrawtk, text="출금", command=submit)
    submit_button.pack()

    result_label = tk.Label(withdrawtk, text="")
    result_label.pack()

    withdrawtk.mainloop()


#송금 함수
def transfer():
    def submit():
        account_num = int(account_entry.get())
        cur.execute("SELECT * FROM TEST WHERE account = ?", (account_num,))
        row = cur.fetchone()

        if row:
            password = password_entry.get()
            enpw = encoding(password)

            if row[4] != enpw:
                result_label.config(text="비밀번호가 틀렸습니다.")
                return

            target_account = int(target_entry.get())
            cur.execute("SELECT * FROM TEST WHERE account = ?", (target_account,))
            target_row = cur.fetchone()

            if target_row:
                amount = int(amount_entry.get())
                current_balance = row[3]
                result_label.config(text=f"{row[1]}님 계좌에는 {current_balance}원이 있습니다. \n {target_row[1]}님 계좌에 {amount}원 송금하시겠습니까?")
                if amount > current_balance:
                    result_label.config(text=f"{row[1]}님 계좌에는 {current_balance}원이 있습니다.\n계좌의 잔액보다 더 큰 금액을 입력했습니다.")
                    return
                elif amount <= 0:
                    result_label.config(text="0보다 더 큰 금액을 입력해 주세요.")
                    return
                def confirm():
                    cur.execute("UPDATE TEST SET balance = balance - ? WHERE account = ?", (amount, account_num))
                    cur.execute("UPDATE TEST SET balance = balance + ? WHERE account = ?", (amount, target_row[0]))
                    cur.execute("INSERT INTO HISTORY VALUES (?, ?, ?, ?, ?)", (row[0], datetime.now(), "송금보냄", amount, target_row[1]))
                    cur.execute("INSERT INTO HISTORY VALUES (?, ?, ?, ?, ?)", (target_row[0], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "송금받음", amount, row[1]))
                    result_label.config(text=f"{amount}원이 송금되었습니다.")
                    root.destroy()
                confirm_button = tk.Button(root, text="확인", command=confirm)
                confirm_button.pack()
                submit_button.pack_forget()
            else:
                result_label.config(text="송금 받을 분의 계좌가 존재하지 않습니다.")
        else:
            result_label.config(text="계좌번호가 틀렸습니다.")

    root = tk.Tk()

    account_label = tk.Label(root, text="계좌번호를 입력해 주세요.")
    account_label.pack()

    account_entry = tk.Entry(root)
    account_entry.pack()

    password_label = tk.Label(root, text="비밀번호를 입력해 주세요.")
    password_label.pack()

    password_entry = tk.Entry(root,show="*")
    password_entry.pack()

    target_label = tk.Label(root, text="어느 계좌로 송금하시겠습니까?")
    target_label.pack()

    target_entry = tk.Entry(root)
    target_entry.pack()

    amount_label = tk.Label(root, text="송금할 금액을 입력해 주세요.")
    amount_label.pack()

    amount_entry = tk.Entry(root)
    amount_entry.pack()

    submit_button = tk.Button(root, text="송금", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()


#잔액 확인 함수
def checkaccount():
    def submit():
        account_num = int(account_entry.get())
        cur.execute("SELECT * FROM TEST WHERE account = ?", (account_num,))
        row = cur.fetchone()
        if row:
            password = password_entry.get()
            enpw = encoding(password)
            if row[4] != enpw:
                result_label.config(text="비밀번호가 틀렸습니다.")
                return
            result_label.config(text=f"{row[1]}님의 잔고는 {row[3]}원 입니다.")
        else:
            result_label.config(text="계좌가 존재하지 않습니다.")

    root = tk.Tk()

    account_label = tk.Label(root, text="계좌번호를 입력해 주세요.")
    account_label.pack()

    account_entry = tk.Entry(root)
    account_entry.pack()

    password_label = tk.Label(root, text="비밀번호를 입력해 주세요.")
    password_label.pack()

    password_entry = tk.Entry(root,show="*")
    password_entry.pack()

    submit_button = tk.Button(root, text="확인", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

#거래 내역 확인 함수
def checkhistory():
    def submit():
        account_num = int(account_entry.get())
        cur.execute("SELECT * FROM TEST WHERE account = ?", (account_num,))
        row = cur.fetchone()

        if row:
            password = password_entry.get()
            enpw = encoding(password)

            if row[4] != enpw:
                result_label.config(text="비밀번호가 틀렸습니다.")
                return

            cur.execute("SELECT * FROM HISTORY WHERE account = ?", (account_num,))
            rows = cur.fetchall()

            if rows:
                result_label.config(text="거래 내역:")
                for row in rows:
                    result_label.config(text=result_label.cget("text") + f"\n{row}")
            else:
                result_label.config(text="거래 내역이 없습니다.")
        else:
            result_label.config(text="계좌가 존재하지 않습니다.")

    root = tk.Tk()

    account_label = tk.Label(root, text="계좌번호를 입력해 주세요.")
    account_label.pack()

    account_entry = tk.Entry(root)
    account_entry.pack()

    password_label = tk.Label(root, text="비밀번호를 입력해 주세요.")
    password_label.pack()

    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    submit_button = tk.Button(root, text="확인", command=submit)
    submit_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

def main():
    root = tk.Tk()
    root.geometry("300x300")
    adduser_button = tk.Button(root, text="계좌 개설", command=adduser)
    adduser_button.pack()

    putmoney_button = tk.Button(root, text="입금", command=putmoney)
    putmoney_button.pack()

    withdraw_button = tk.Button(root, text="출금", command=withdraw)
    withdraw_button.pack()

    transfer_button = tk.Button(root, text="송금", command=transfer)
    transfer_button.pack()

    checkaccount_button = tk.Button(root,text="계좌 잔액 확인",command=checkaccount)
    checkaccount_button.pack()

    check_history_button = tk.Button(root, text="거래내역 확인", command=checkhistory)
    check_history_button.pack()
    root.mainloop()

main()
df = pd.read_sql_query("SELECT * FROM TEST", conn)
print(*df.to_dict("records"), sep="\n")