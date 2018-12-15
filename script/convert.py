import os
import sys


def gen_md(filename):
    pandoc = "pandoc -f mediawiki -t markdown {filename}.txt -o {filename}.md"
    os.system(pandoc.format(filename=filename))


def gen_secs(filename):
    def write(sec_id):
        res = "{}_{}".format(filename, sec_id)
        with open(res + ".md", 'w') as fw:
            if first_line:
                fw.write(first_line + content)
            else:
                fw.write(content)
        pandoc = "pandoc -f markdown -t html {filename}.md -o {filename}.html"
        os.system(pandoc.format(filename=res))
        print("Generated {}".format(res))
        return res.replace('_', '.')

    sec_id = 0
    files = []
    with open(filename + ".md") as f:
        first_line = None
        content = ""
        for line in f:
            if line.startswith("### "):
                if first_line or content:
                    files.append(write(sec_id))
                    sec_id += 1
                first_line = line
                content = ""
            else:
                content += line
        if first_line or content:
            files.append(write(sec_id))
    return files


if __name__ == '__main__':
    files = []
    for filename in range(2, 22):
        filename = str(filename)
        gen_md(filename)
        files += gen_secs(filename)
    with open("toc.txt", 'w') as f:
        f.write('\n'.join(files))
