

with open("export/part/exp1", "r") as first:
    with open("export/part/exp2", "r") as second:
        r_first = first.readlines()
        r_second = second.readlines()

        for mail_first in r_first:
            did_both = False
            for mail_second in r_second:
                if mail_first.strip() == mail_second.strip():
                    did_both = True

            if did_both:
                print(mail_first, end="")
