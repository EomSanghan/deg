#ticketing_user
import tkinter as tk
from tkinter import messagebox, simpledialog
import pprint

# 큐 구현을 위한 Queue 클래스
class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self._data.pop(0)
        else:
            raise Exception("Queue is empty")

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

# 예약정보DB 구현을 위한 ReservationInfo 클래스
class ReservationInfo:
    def __init__(self, performance_name):
        self.performance_name = performance_name
        self.queue = Queue()  # 대기리스트DB를 위한 큐
        self.reservations = {}  # 예약정보DB를 위한 해시테이블(딕셔너리)

    def add_waitlist(self, name): # 대기리스트(큐)에 추가
        self.queue.enqueue(name)

    def add_reservation(self, name, seat_name, show_info=True): # 해시테이블(딕셔너리)에 이름, 좌석, 공연정보 저장
        self.reservations[name] = {'performance': self.performance_name, 'seat': seat_name}
        if show_info:
            self.show_info(name)

    def remove_reservation(self, name): # 예매취소기능
        if name in self.reservations:
            seat_name = self.reservations[name]['seat']
            del self.reservations[name]
            messagebox.showinfo("예매 취소", f"예매 취소: {name}, {self.performance_name}, {seat_name}")
            return seat_name
        return None

    def get_waiting_user(self): # 예약취소로 생긴 좌석에 대기리스트 순번대로 자동 예약하기 위해 큐에서 이름을 받아옴
        return self.queue.dequeue() if not self.queue.is_empty() else None

    def show_info(self, name): # 예매정보확인
        if name in self.reservations:
            info = f"예매 정보\n이름: {name}\n공연명: {self.reservations[name]['performance']}\n좌석: {self.reservations[name]['seat']}"
            messagebox.showinfo("예매 정보", info)
        elif name in self.queue._data:
            info = f"{name}님은 대기자리스트에 있습니다."
            messagebox.showinfo("대기자리스트 정보", info)
        else:
            messagebox.showinfo("정보 없음", f"{name}님의 예매정보가 존재하지 않습니다.")

# 공연과 각 공연에 대한 예약기능 구현을 위한 Performance 클래스
class Performance:
    def __init__(self, name):
        self.name = name
        self.reserved_num = 4
        self.rows_num = 2
        self.cols_num = 2
        self.seats = [[True for _ in range(self.cols_num)] for _ in range(self.rows_num)] # 좌석의 행,열 크기를 갖는 2차원 리스트를 반환하고 모두 True로 초기화
        self.reservation_info = ReservationInfo(name) 
    
    def reservation(self, username, seat_name):
        if self.reserved_num != 0:
            row_index, col_index = self.find_seat(seat_name)
            if row_index is None or col_index is None:
                return
            if self.seats[row_index][col_index]:
                if messagebox.askyesno("예매 확인", "빈 좌석입니다. 예매를 진행하시겠습니까?"):
                    self.seats[row_index][col_index] = False
                    self.reserved_num -= 1
                    seat_name = f"{chr(row_index + ord('A'))}{col_index + 1}" # 좌석 행렬 정보를 다시 입력받은 좌석정보로 변환 ord() : 알파벳의 유니코드 코드 포인트 반환, chr() 유니코드 코드 포인트를 알파벳으로 변환
                    self.reservation_info.add_reservation(username, seat_name, show_info=False)
                    messagebox.showinfo("예매 완료", "예매가 완료되었습니다.")
                    self.reservation_info.show_info(username)
                    return True
            else:
                messagebox.showwarning("예매 불가", "이미 예매완료된 좌석입니다. 다른 좌석을 선택해주세요.")
        else:
            if messagebox.askyesno("예매 대기", "모든 좌석이 예매되었습니다. 예약대기 신청을 하시겠습니까?"):
                self.reservation_info.add_waitlist(username)
                messagebox.showinfo("대기자 등록", f"{username}님이 대기자 리스트에 추가되었습니다.")
        return False
    
    def find_seat(self, seat_name):
        try:
            row_index = ord(seat_name[0].upper()) - ord('A') 
            col_index = int(seat_name[1:]) - 1
            if 0 <= row_index < self.rows_num and 0 <= col_index < self.cols_num:
                return row_index, col_index
            else:
                messagebox.showerror("잘못된 입력", "유효한 좌석 번호를 입력하세요.")
                return None, None
        except (IndexError, ValueError):
            messagebox.showerror("잘못된 입력", "유효한 좌석 번호를 입력하세요.")
            return None, None

    def cancel_reserve(self, username):
        seat_name = self.reservation_info.remove_reservation(username)
        if seat_name:
            row_index = ord(seat_name[0]) - ord('A')
            col_index = int(seat_name[1:]) - 1
            self.seats[row_index][col_index] = True
            self.reserved_num += 1
            messagebox.showinfo("예매 취소", f"{username}님의 예매가 취소되었습니다.")
            next_user = self.reservation_info.get_waiting_user()
            if next_user:
                self.auto_reservation(next_user)
        else:
            messagebox.showwarning("취소 불가", f"{username}님의 예매정보가 존재하지 않습니다.")

    def auto_reservation(self, username):
        for row in range(self.rows_num):
            for col in range(self.cols_num):
                if self.seats[row][col]:
                    seat_name = f"{chr(row + ord('A'))}{col + 1}"
                    self.seats[row][col] = False
                    self.reserved_num -= 1
                    self.reservation_info.add_reservation(username, seat_name, show_info=False)
                    return

    def available_seats(self):
        available = []
        for row in range(self.rows_num):
            for col in range(self.cols_num):
                if self.seats[row][col]:
                    available.append(f"{chr(row + ord('A'))}{col + 1}")
        return ", ".join(available)

    def show_reservation_info(self, name):
        self.reservation_info.show_info(name)

# GUI 구현을 위한 TicketingApp 클래스
class ticketing_user_gui:
    def __init__(self, root):
        self.root = root
        self.root.title("공연 티켓팅 시스템")

        self.performances = {
            '공연1(2024-06-07)': Performance('공연1(2024-06-07)'),
            '공연2(2024-07-13)': Performance('공연2(2024-07-13)'),
            '공연3(2024-08-20)': Performance('공연3(2024-08-20)')
        }

        self.selected_performance = tk.StringVar()
        self.selected_performance.set('공연1(2024-06-07)')
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="예매를 원하는 공연을 선택해주세요").pack(pady=10)
        
        for perf in self.performances.keys():
            tk.Radiobutton(self.root, text=perf, variable=self.selected_performance, value=perf).pack(anchor=tk.W)

        tk.Label(self.root, text="ID를 입력해주세요").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Button(self.root, text="예매", command=self.book_ticket).pack(pady=5)
        tk.Button(self.root, text="예매 취소", command=self.cancel_ticket).pack(pady=5)
        tk.Button(self.root, text="예매 가능한 좌석 확인", command=self.show_available_seats).pack(pady=5)
        tk.Button(self.root, text="예매 정보 확인", command=self.show_info).pack(pady=5)

    def book_ticket(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("입력 오류", "예매하신 고객님의 ID를 입력해주세요.")
            return

        perf = self.selected_performance.get()
        seat_name = simpledialog.askstring("좌석 입력", "좌석을 입력해주세요 (예: A1):")
        if seat_name:
            self.performances[perf].reservation(username, seat_name)

    def cancel_ticket(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("입력 오류", "예매하신 고객님의 ID를 입력해주세요.")
            return

        perf = self.selected_performance.get()
        self.performances[perf].cancel_reserve(username)

    def show_info(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("입력 오류", "예매하신 고객님의 ID를 입력해주세요.")
            return

        perf = self.selected_performance.get()
        self.performances[perf].show_reservation_info(username)

    def show_available_seats(self):
        perf = self.selected_performance.get()
        available_seats = self.performances[perf].available_seats()
        messagebox.showinfo("예매 가능한 좌석", available_seats)

if __name__ == "__main__":
    root = tk.Tk()
    app = ticketing_user_gui(root)
    root.mainloop()
