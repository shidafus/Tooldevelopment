import difflib,sys


def compare_files(file_name_x, file_name_y):
    # read files and split content into lists of strings for each line
    try:
        text_file = open(str(file_name_x), "r", encoding="utf-8")
        first_text_lines = text_file.read().splitlines(keepends=True)

        text_file = open(str(file_name_y), "r", encoding="utf-8")
        second_text_lines = text_file.read().splitlines(keepends=True)

        # create diff object and calculate diff content
        d = difflib.Differ()
        difference = list(d.compare(first_text_lines, second_text_lines))
        # html_report = difflib.HtmlDiff(wrapcolumn=80).make_file(first_text_lines, second_text_lines)

    except Exception as e:
        print("Cannot read file : ", str(e))

    return ''.join([x.replace('\\', '\\\\') for x in difference])
    # return html_report


if len(sys.argv) != 3:
    print(f"Please enter the format of python {sys.argv[0]} file1 file2")
    sys.exit()

with open(r'C:\Users\zhoujiahao\Desktop\diff.html', 'w', encoding='utf-8') as f:
   result_html = compare_files(sys.argv[1], sys.argv[2])
   f.write(result_html)

# result = compare_files('C:\\Users\\Administrator\\Desktop\\1.txt', 'C:\\Users\\Administrator\\Desktop\\2.txt')
# print(result)