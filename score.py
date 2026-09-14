def input_number(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("숫자만 입력해주세요. 다시 입력해주세요.")


def main():
    name = input("학생 이름을 입력하세요: ")

    korean = input_number("국어 점수를 입력하세요: ")
    english = input_number("영어 점수를 입력하세요: ")
    math = input_number("수학 점수를 입력하세요: ")

    average = (korean + english + math) / 3

    print(f"\n{name} 학생의 평균 점수는 {average:.2f}점입니다.")


if __name__ == "__main__":
    main()
