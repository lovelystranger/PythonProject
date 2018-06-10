import os 
def append_text(text):
	f = open('alan_diary.log','a')
	f.write(text + '\n')
	f.close()

def get_text():
	if not os.path.exists('alan_diary.log'):
		append_text('')
	else:
		f = open('alan_diary.log')
		text = f.read()
		f.close()
		return text

if __name__ == '__main__':
	while True:
		text_input = input("what do you want to write today:\n>")
		if text_input.lower() in ['quit','q','exit']:break
		append_text(text_input)
		print("your diary:\n",get_text())