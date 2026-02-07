def normalize(s):
    return s.strip().replace("\r\n", "\n")

def check_output(user_out, expected_out):
    return normalize(user_out) == normalize(expected_out)