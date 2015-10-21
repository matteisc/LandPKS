import hashlib, random, string

# Calculate a Drupal 7 compatible password hash.

class DrupalHash:

    def __init__(self):
        self.itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.min_log = 7
        self.max_log = 30
        self.default_log = 15
        self.hash_length = 55
    
    def password_get_count_log2(self, setting):
        return self.itoa64.index(setting[3])

    def password_crypt(self, algo, password, setting):
        password = password.decode('utf-8').encode('utf-8')
        setting = setting[0:12]
        if setting[0] != '$' or setting[2] != '$':
            return False

        count_log2 = self.password_get_count_log2(setting)
        salt = setting[4:12]
        if len(salt) < 8:
            return False
        count = 1 << count_log2

        if algo == 'md5':
            hash_func = hashlib.md5
        elif algo == 'sha512':
            hash_func = hashlib.sha512
        else:
            return False
        hash_str = hash_func(salt + password).digest()
        for c in range(count):
            hash_str = hash_func(hash_str + password).digest()
        output = setting + self.custom64(hash_str)
        return output[0:self.hash_length]

    def custom64(self, string, count = 0):
        if count == 0:
            count = len(string)
        output = ''
        i = 0
        itoa64 = self.itoa64
        while 1:
            value = ord(string[i])
            i += 1
            output += itoa64[value & 0x3f]
            if i < count:
                value |= ord(string[i]) << 8
            output += itoa64[(value >> 6) & 0x3f]
            if i >= count:
                break
            i += 1
            if i < count:
                value |= ord(string[i]) << 16
            output += itoa64[(value >> 12) & 0x3f]
            if i >= count:
                break
            i += 1
            output += itoa64[(value >> 18) & 0x3f]
            if i >= count:
               break
        return output

    def rehash(self, stored_hash, password):
        # Drupal 6 compatibility
        if len(stored_hash) == 32 and stored_hash.find('$') == -1:
            return hashlib.md5(password).hexdigest()
        # Drupal 7
        if stored_hash[0:2] == 'U$':
            stored_hash = stored_hash[1:]
            password = hashlib.md5(password).hexdigest()
        hash_type = stored_hash[0:3]
        if hash_type == '$S$':
            hash_str = self.password_crypt('sha512', password, stored_hash)
        elif hash_type == '$H$' or hash_type == '$P$':
            hash_str = self.password_crypt('md5', password, stored_hash)
        else:
            hash_str = False
        return hash_str

    def password_generate_salt(self, count_log2):
        output = '$S$'
        count_log2 = self._password_enforce_log2_boundaries(count_log2)
        output += self.itoa64[count_log2]
        output += self.custom64(self._random_string(6), 6)
        return output
    def user_check_password(self,check_password,stored_password):
        hash = self.password_crypt('sha512', check_password, stored_password);
        if (stored_password.strip() == hash.strip()):
            return True
        else:
            return False
    def user_hash_password(self, password, count_log2 = 0):
        if count_log2 == 0:
            count_log2 = self.default_log
        return self.password_crypt('sha512', password, self.password_generate_salt(count_log2))
        
    def _password_enforce_log2_boundaries(self, count_log2):
        if count_log2 < self.min_log:
            return self.min_log
        if count_log2 > self.max_log:
            return self.max_log
        return count_log2

    def _random_string(self, length):
        r = random.SystemRandom()
        chars = string.letters + string.digits
        return ''.join(r.choice(chars) for _ in xrange(length))
