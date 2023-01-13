import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check your API and try again.')
    return response

def get_pw_leaks_count(hash_results, hash_to_count):
    hashes = (line.split(':') for line in hash_results.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_count:
            return count
    return 0

def pwned_api_check(password):
    sha1_pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    query_char, tail = sha1_pw[:5], sha1_pw[5:]
    response = request_api_data(query_char)
    return get_pw_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'Password \'{password}\' has been pawned {count} times... you probably want to change your password.')
        else:
            print(f'Password \'{password}\' has never been pawned. You\'re good to go.')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

