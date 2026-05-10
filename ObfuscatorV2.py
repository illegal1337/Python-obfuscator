# Made by 1337 Team in 2024
# If u steal our source give credits please <3
import base64
import zlib
import random
import string
import marshal
import math
import sys
import os
from colorama import init as _colorama_init, Fore, Style

_colorama_init(autoreset=True)

# Blood-red and orange ANSI via colorama-compatible escape sequences
RED    = "\033[38;2;180;0;0m"      # blood red
ORANGE = "\033[38;2;255;140;0m"    # orange
BRED   = "\033[38;2;220;20;20m"    # bright blood red (accents)
DIM    = Style.DIM
RESET  = Style.RESET_ALL
BOLD   = Style.BRIGHT

variable_names = "__1337s__"

def random_var(length=16):
    return '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 1 — Marshal + THREE chaotic maps + Fibonacci seeds + CBC feedback + Base85
# ─────────────────────────────────────────────────────────────────────────────
def layer1_marshal_logistic_b85(code_string):
    compiled = compile(code_string, '<x>', 'exec')
    raw = marshal.dumps(compiled)
    n = len(raw)

    phi = 1.6180339887498948

    x01 = round(random.uniform(0.02, 0.97), 15)
    x02 = round((x01 * phi) % 1.0, 15)
    x03 = round((x02 * phi * phi) % 1.0, 15)
    omega = round(random.uniform(0.1, 0.9), 10)
    K     = round(random.uniform(0.5, 2.5), 10)

    x = x01
    s1 = []
    for _ in range(n):
        x = 3.9999 * x * (1 - x)
        s1.append(int(x * 256) % 256 or 1)
    xored1 = bytes([b ^ s for b, s in zip(raw, s1)])

    x = x02
    s2 = []
    for _ in range(n):
        x = 2 * x if x < 0.5 else 2 * (1 - x)
        s2.append(int(x * 256) % 256 or 1)
    xored2 = bytes([b ^ s for b, s in zip(xored1, s2)])

    x = x03
    s3 = []
    K2pi = K / (2 * math.pi)
    for _ in range(n):
        x = (x + omega - K2pi * math.sin(2 * math.pi * x)) % 1.0
        s3.append(int(x * 256) % 256 or 1)
    xored3 = bytes([b ^ s for b, s in zip(xored2, s3)])

    iv = random.randint(1, 255)
    cbc = bytearray(n)
    prev = iv
    for i, b in enumerate(xored3):
        cbc[i] = b ^ prev
        prev = cbc[i]
    final = bytes(cbc)

    encoded = base64.b85encode(final).decode()

    vx1 = random_var(); vs1 = random_var()
    vx2 = random_var(); vs2 = random_var()
    vx3 = random_var(); vs3 = random_var()
    vd  = random_var(); vd2 = random_var(); vd3 = random_var()
    vd4 = random_var(); vi  = random_var(); vprev = random_var()

    parts = [
        "import marshal,base64,math;",
        f"{vx1}=[{repr(x01)}];{vs1}=[];",
        f"[({vx1}.__setitem__(0,3.9999*{vx1}[0]*(1-{vx1}[0])),{vs1}.append(int({vx1}[0]*256)%256 or 1))"
        f"for _ in range({n})];",
        f"{vx2}=[{repr(x02)}];{vs2}=[];",
        f"[({vx2}.__setitem__(0,2*{vx2}[0] if {vx2}[0]<0.5 else 2*(1-{vx2}[0])),{vs2}.append(int({vx2}[0]*256)%256 or 1))"
        f"for _ in range({n})];",
        f"{vx3}=[{repr(x03)}];{vs3}=[];",
        f"[({vx3}.__setitem__(0,({vx3}[0]+{repr(omega)}-({repr(K)}/(2*math.pi))*math.sin(2*math.pi*{vx3}[0]))%1.0),{vs3}.append(int({vx3}[0]*256)%256 or 1))"
        f"for _ in range({n})];",
        f"{vd}=base64.b85decode('{encoded}');",
        f"{vd2}=bytearray({n});",
        f"{vprev}=[{iv}];",
        f"[({vd2}.__setitem__({vi},{vd}[{vi}]^({vprev}[0] if {vi}==0 else {vd}[{vi}-1])))"
        f"for {vi} in range({n})];",
        f"{vd2}=bytes({vd2});",
        f"{vd3}=bytes([a^b for a,b in zip({vd2},{vs3})]);",
        f"{vd4}=bytes([a^b for a,b in zip({vd3},{vs2})]);",
        f"exec(marshal.loads(bytes([a^b for a,b in zip({vd4},{vs1})])));",
    ]
    return ''.join(parts)

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 2 — Zlib + TWO random Base64 alphabets + Bit rotation + Nibble swap
# ─────────────────────────────────────────────────────────────────────────────
def layer2_custom_b64_bitrot(code_string):
    compressed   = zlib.compress(code_string.encode(), 9)
    standard_b64 = base64.b64encode(compressed).decode()

    std_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    custom_list1 = list(std_alpha)
    random.shuffle(custom_list1)
    custom_alpha1 = ''.join(custom_list1)
    b64_custom1 = standard_b64.translate(str.maketrans(std_alpha, custom_alpha1))

    rot_k   = random.randint(1, 7)
    rotated = bytes([((ord(c) << rot_k) | (ord(c) >> (8 - rot_k))) & 0xFF for c in b64_custom1])

    pos_p = random.choice([7, 11, 13, 17, 19, 23])
    pos_q = random.randint(1, 127)
    xored = bytes([(b ^ ((i * pos_p + pos_q) % 256)) for i, b in enumerate(rotated)])

    nibble_swapped = bytes([((b & 0x0F) << 4) | ((b & 0xF0) >> 4) for b in xored])

    chunk_sz = random.randint(4, 9)
    chunked = bytearray()
    for i in range(0, len(nibble_swapped), chunk_sz):
        chunked += nibble_swapped[i:i+chunk_sz][::-1]
    chunk_reversed = bytes(chunked)

    second_alpha_list = list(range(256))
    random.shuffle(second_alpha_list)
    inv_second_alpha = [0] * 256
    for i, v in enumerate(second_alpha_list):
        inv_second_alpha[v] = i

    final = bytes([second_alpha_list[b] for b in chunk_reversed])
    hex_enc = final.hex()

    inv2_str = ','.join(str(x) for x in inv_second_alpha)

    v1 = random_var(); v2 = random_var(); v3 = random_var()
    v4 = random_var(); v5 = random_var(); v6 = random_var()
    v7 = random_var(); v8 = random_var(); v9 = random_var()
    vchk = random_var(); vrev = random_var()

    return (
        f"import zlib,base64;"
        f"{v9}=[{inv2_str}];"
        f"{v1}=str.maketrans('{custom_alpha1}','{std_alpha}');"
        f"{v2}=bytes.fromhex('{hex_enc}');"
        f"{v7}=bytes([{v9}[b] for b in {v2}]);"
        f"{vchk}=bytearray();"
        f"[{vchk}.__iadd__({v7}[i:i+{chunk_sz}][::-1])for i in range(0,len({v7}),{chunk_sz})];"
        f"{vrev}=bytes({vchk});"
        f"{v8}=bytes([((b&0x0F)<<4)|((b&0xF0)>>4) for b in {vrev}]);"
        f"{v3}=bytes([(b^((i*{pos_p}+{pos_q})%256)) for i,b in enumerate({v8})]);"
        f"{v4}=bytes([((b>>{rot_k})|(b<<{8-rot_k}))&255 for b in {v3}]).decode();"
        f"{v5}={v4}.translate({v1});"
        f"{v6}=zlib.decompress(base64.b64decode({v5}));"
        f"exec({v6})"
    )

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3 — Sub + Vigenere + Double transposition + RC4-like stream + Sub2 + Hex
# ─────────────────────────────────────────────────────────────────────────────
def layer3_sub_vig_transpose_hex(code_string):
    data = code_string.encode()

    sub_table = list(range(256))
    random.shuffle(sub_table)
    inv_table = [0] * 256
    for i, v in enumerate(sub_table):
        inv_table[v] = i

    vig_key = [random.randint(1, 255) for _ in range(random.randint(32, 64))]
    vig_len = len(vig_key)
    after_sub_vig = bytes(
        [(sub_table[b] + vig_key[i % vig_len]) % 256 for i, b in enumerate(data)]
    )

    n_cols1 = random.randint(5, 13)
    pad1    = (-len(after_sub_vig)) % n_cols1
    padded1 = after_sub_vig + bytes([0] * pad1)
    nrows1  = len(padded1) // n_cols1
    trans1  = bytes([padded1[r * n_cols1 + c] for c in range(n_cols1) for r in range(nrows1)])

    n_cols2 = random.randint(6, 15)
    while n_cols2 == n_cols1:
        n_cols2 = random.randint(6, 15)
    pad2    = (-len(trans1)) % n_cols2
    padded2 = trans1 + bytes([0] * pad2)
    nrows2  = len(padded2) // n_cols2
    trans2  = bytes([padded2[r * n_cols2 + c] for c in range(n_cols2) for r in range(nrows2)])

    rc4_key = [random.randint(0, 255) for _ in range(random.randint(16, 32))]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + rc4_key[i % len(rc4_key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    rc4_stream = []
    for _ in range(len(trans2)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        rc4_stream.append(S[(S[i] + S[j]) % 256])
    after_rc4 = bytes([b ^ k for b, k in zip(trans2, rc4_stream)])

    sub2 = list(range(256))
    random.shuffle(sub2)
    inv2 = [0] * 256
    for i, v in enumerate(sub2):
        inv2[v] = i
    after_sub2 = bytes([sub2[b] for b in after_rc4])

    hex_str  = after_sub2.hex()[::-1]
    orig_len = len(data)
    len_trans1 = len(trans1)
    len_trans2 = len(trans2)

    inv_str  = ','.join(str(x) for x in inv_table)
    vig_str  = ','.join(str(k) for k in vig_key)
    inv2_str = ','.join(str(x) for x in inv2)

    n_stream_frags = random.randint(4, 7)
    stream_bytes   = bytes(rc4_stream)
    sf_size        = max(1, len(stream_bytes) // n_stream_frags)
    stream_parts   = [stream_bytes[i:i+sf_size] for i in range(0, len(stream_bytes), sf_size)]
    sf_keys        = [random.randint(1, 254) for _ in stream_parts]
    sf_hex         = [bytes([b ^ sf_keys[i] for b in part]).hex()
                      for i, part in enumerate(stream_parts)]
    sf_vars        = [random_var() for _ in stream_parts]
    n_sf_decoys    = random.randint(3, 6)
    sfd_vars       = [random_var() for _ in range(n_sf_decoys)]
    sfd_hex        = [bytes([random.randint(0,255) for _ in range(sf_size)]).hex()
                      for _ in range(n_sf_decoys)]
    sf_all = list(zip(sf_vars, sf_hex)) + list(zip(sfd_vars, sfd_hex))
    random.shuffle(sf_all)
    sf_assign = ';'.join(f"{v}='{h}'" for v, h in sf_all)
    sf_reassemble = '+'.join(
        f"bytes([b^{sf_keys[i]} for b in bytes.fromhex({v})])"
        for i, v in enumerate(sf_vars)
    )

    v1  = random_var(); v2  = random_var(); v3  = random_var()
    v4  = random_var(); v5  = random_var(); v6  = random_var()
    v7  = random_var(); v8  = random_var(); v9  = random_var()
    v10 = random_var(); v11 = random_var(); vst = random_var()

    return (
        f"{v1}=[{inv_str}];"
        f"{v2}=[{vig_str}];"
        f"{v7}=[{inv2_str}];"
        f"{sf_assign};"
        f"{vst}={sf_reassemble};"
        f"{v3}=bytes.fromhex('{hex_str}'[::-1]);"
        f"{v8}=bytes([{v7}[b] for b in {v3}]);"
        f"{v9}=bytes([b^k for b,k in zip({v8},{vst})]);"
        f"{v10}=len({v9})//{n_cols2};"
        f"{v11}=bytes([{v9}[(i%{n_cols2})*{v10}+i//{n_cols2}]for i in range({v10}*{n_cols2})])[:{len_trans1}];"
        f"{v4}=len({v11})//{n_cols1};"
        f"{v5}=bytes([{v11}[(i%{n_cols1})*{v4}+i//{n_cols1}]for i in range({v4}*{n_cols1})])[:{orig_len}];"
        f"{v6}=bytes([{v1}[(b-{v2}[i%{vig_len}])%256]for i,b in enumerate({v5})]);"
        f"exec({v6})"
    )

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 4 — Zlib + Base85 + Chained XOR fragments + Functional decoys
# ─────────────────────────────────────────────────────────────────────────────
def layer4_decoy_xor_fragments(code_string):
    compressed = zlib.compress(code_string.encode(), 9)
    encoded    = base64.b85encode(compressed).decode()

    n_real  = random.randint(7, 12)
    n_decoy = random.randint(10, 16)

    size       = max(1, len(encoded) // n_real)
    real_parts = [encoded[i:i+size] for i in range(0, len(encoded), size)]

    key_init = random.randint(2, 253)
    chain_p  = random.choice([3, 5, 7, 11, 13])

    frag_keys = []
    k = key_init
    for i in range(len(real_parts)):
        frag_keys.append(k)
        k = ((k ^ ((i + 1) * chain_p)) % 254) + 1

    accum = 0
    final_hex_reals = []
    for i, part in enumerate(real_parts):
        dep_key = (frag_keys[i] ^ accum) % 256 or 1
        enc = bytes([ord(c) ^ dep_key for c in part])
        final_hex_reals.append(enc.hex())
        accum = (accum + enc[0]) % 256
    eff_keys = []
    accum = 0
    for i, part in enumerate(real_parts):
        dep_key = (frag_keys[i] ^ accum) % 256 or 1
        eff_keys.append(dep_key)
        enc = bytes([ord(c) ^ dep_key for c in part])
        accum = (accum + enc[0]) % 256
    hex_reals = final_hex_reals

    frag_len    = len(hex_reals[0]) // 2
    decoy_hexes = [
        bytes([random.randint(0, 255) for _ in range(frag_len)]).hex()
        for _ in range(n_decoy)
    ]
    fake_keys   = [random.randint(1, 255) for _ in range(n_decoy)]

    real_vars  = [random_var() for _ in real_parts]
    decoy_vars = [random_var() for _ in range(n_decoy)]

    all_assigns = (
        [(v, h, None)     for v, h in zip(real_vars, hex_reals)] +
        [(v, h, fake_keys[i]) for i, (v, h) in enumerate(zip(decoy_vars, decoy_hexes))]
    )
    random.shuffle(all_assigns)

    join_var = random_var()
    res_var  = random_var()

    assign_parts = []
    for v, h, fk in all_assigns:
        assign_parts.append(f"{v}='{h}'")
    assign = ';'.join(assign_parts)

    decode_parts = [
        f"''.join(chr(b^{eff_keys[i]})for b in bytes.fromhex({v}))"
        for i, v in enumerate(real_vars)
    ]
    join_expr = '+'.join(decode_parts)

    return (
        f"import zlib,base64;"
        f"{assign};"
        f"{join_var}={join_expr};"
        f"{res_var}=zlib.decompress(base64.b85decode({join_var}));"
        f"exec({res_var})"
    )

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 5 — Dual LCG + Visual repeated-variable noise shell
# ─────────────────────────────────────────────────────────────────────────────
def layer5_encrypted_visual(code_string):
    repeat_name = variable_names.strip() if variable_names.strip() else "__1337s__"

    seed1 = random.randint(10000, 9999999)
    seed2 = random.randint(10000, 9999999)
    key_len = random.randint(16, 28)
    mult1, inc1 = 1664525,  1013904223
    mult2, inc2 = 22695477, 1

    state1, state2 = seed1, seed2
    key = []
    for _ in range(key_len):
        state1 = (state1 * mult1 + inc1) & 0xFFFFFFFF
        state2 = (state2 * mult2 + inc2) & 0xFFFFFFFF
        byte   = ((state1 >> 16) ^ (state2 >> 8)) & 0xFF
        key.append(byte if byte > 0 else 1)

    encrypted = bytes([b ^ key[i % key_len] for i, b in enumerate(code_string.encode())])

    chunk_size = random.randint(16, 24)
    int_chunks = [
        list(encrypted[i:i+chunk_size])
        for i in range(0, len(encrypted), chunk_size)
    ]

    data_var   = random_var()
    s1_var     = random_var()
    s2_var     = random_var()
    key_var    = random_var()
    loop_var   = '_' + random_var(5)
    result_var = random_var()

    def rep(n=None):
        if n is None:
            n = random.randint(8, 18)
        return " ; ".join(f"{repeat_name} = '{repeat_name}'" for _ in range(n))

    def pad(lo=1, hi=2):
        for _ in range(random.randint(lo, hi)):
            L.append(rep())

    L = []

    pad(4, 7)

    L.append(f"{data_var} = b''")
    # Only add per-chunk padding when the number of chunks is small enough
    # to avoid generating hundreds of MB of output.
    per_chunk_pad = len(int_chunks) < 400
    for chunk in int_chunks:
        if per_chunk_pad:
            pad(1, 2)
        L.append(f"{data_var} += bytes({chunk})")

    pad(3, 6)
    L.append(f"{s1_var} = {seed1}")
    pad(2, 4)
    L.append(f"{s2_var} = {seed2}")
    pad(2, 4)
    L.append(f"{key_var} = []")
    pad(2, 4)
    L.append(f"for {loop_var} in range({key_len}):")
    L.append(f"    {s1_var} = ({s1_var} * {mult1} + {inc1}) & 0xFFFFFFFF")
    L.append(f"    {s2_var} = ({s2_var} * {mult2} + {inc2}) & 0xFFFFFFFF")
    L.append(f"    {key_var}.append((({s1_var} >> 16) ^ ({s2_var} >> 8)) & 255 or 1)")

    pad(2, 4)
    L.append(f"{result_var} = bytes([b ^ {key_var}[i % len({key_var})] for i, b in enumerate({data_var})])")
    pad(2, 4)
    L.append(f"exec({result_var})")

    pad(3, 6)

    return '\n'.join(L)

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 6 — ChaCha20-like quarter-round + BLAKE2-style hash integrity guard
#
#   1) 256-bit key derivation via ARX (Add-Rotate-XOR) mixing with a
#      ChaCha20-inspired quarter-round function.
#   2) Payload is encrypted with the keystream derived from the 16-word state.
#   3) A polynomial integrity hash (mod large Mersenne prime) is embedded;
#      the stub verifies it before executing — any altered byte causes a
#      silent abort.
#   4) The key is split into 8 fragments mixed with equal-length decoys;
#      the assembly order is encoded as an XOR'd permutation.
#   5) The stub regenerates the full keystream, verifies the hash, and runs.
# ─────────────────────────────────────────────────────────────────────────────
def layer6_chacha_arx_integrity(code_string):
    data = code_string.encode()
    n    = len(data)

    # ── ChaCha20-like keystream ───────────────────────────────────────────────
    key256  = [random.randint(0, 0xFFFFFFFF) for _ in range(8)]
    nonce96 = [random.randint(0, 0xFFFFFFFF) for _ in range(3)]
    ctr     = random.randint(0, 0xFFFF)

    SIGMA = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]

    def rotl32(v, n):
        return ((v << n) | (v >> (32 - n))) & 0xFFFFFFFF

    def quarter_round(a, b, c, d):
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = rotl32(d, 16)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = rotl32(b, 12)
        a = (a + b) & 0xFFFFFFFF; d ^= a; d = rotl32(d,  8)
        c = (c + d) & 0xFFFFFFFF; b ^= c; b = rotl32(b,  7)
        return a, b, c, d

    def chacha_block(state):
        ws = list(state)
        for _ in range(10):
            ws[0],ws[4],ws[8],ws[12]  = quarter_round(ws[0],ws[4],ws[8],ws[12])
            ws[1],ws[5],ws[9],ws[13]  = quarter_round(ws[1],ws[5],ws[9],ws[13])
            ws[2],ws[6],ws[10],ws[14] = quarter_round(ws[2],ws[6],ws[10],ws[14])
            ws[3],ws[7],ws[11],ws[15] = quarter_round(ws[3],ws[7],ws[11],ws[15])
            ws[0],ws[5],ws[10],ws[15] = quarter_round(ws[0],ws[5],ws[10],ws[15])
            ws[1],ws[6],ws[11],ws[12] = quarter_round(ws[1],ws[6],ws[11],ws[12])
            ws[2],ws[7],ws[8],ws[13]  = quarter_round(ws[2],ws[7],ws[8],ws[13])
            ws[3],ws[4],ws[9],ws[14]  = quarter_round(ws[3],ws[4],ws[9],ws[14])
        return [(ws[i] + state[i]) & 0xFFFFFFFF for i in range(16)]

    keystream = bytearray()
    block_ctr = ctr
    while len(keystream) < n:
        state = SIGMA + key256 + [block_ctr] + nonce96
        block = chacha_block(state)
        for w in block:
            keystream += w.to_bytes(4, 'little')
        block_ctr += 1

    ciphertext = bytes([data[i] ^ keystream[i] for i in range(n)])

    # ── Polynomial integrity hash ─────────────────────────────────────────────
    PRIME  = (1 << 61) - 1
    BASE   = random.randint(0x1000, 0xFFFF)
    h      = 0
    for b in ciphertext:
        h = (h * BASE + b) % PRIME

    # ── Split key into 8 fragments mixed with decoys ──────────────────────────
    key_bytes   = b''.join(w.to_bytes(4, 'little') for w in key256)
    nonce_bytes = b''.join(w.to_bytes(4, 'little') for w in nonce96)
    n8 = 4  # bytes per key fragment
    key_frags   = [key_bytes[i:i+n8] for i in range(0, len(key_bytes), n8)]
    frag_xk     = [random.randint(1, 253) for _ in key_frags]
    frag_enc    = [bytes([b ^ frag_xk[i] for b in frag]) for i, frag in enumerate(key_frags)]

    n_decoys = random.randint(4, 8)
    decoy_frags = [bytes([random.randint(0,255) for _ in range(n8)]) for _ in range(n_decoys)]

    fv = [random_var() for _ in key_frags]
    dv = [random_var() for _ in decoy_frags]
    all_frags = list(zip(fv, frag_enc)) + list(zip(dv, decoy_frags))
    random.shuffle(all_frags)

    ct_hex   = ciphertext.hex()
    nonce_hex = nonce_bytes.hex()

    vct   = random_var(); vks  = random_var(); vkey = random_var()
    vnon  = random_var(); vctr = random_var(); vblk = random_var()
    vst   = random_var(); vw   = random_var(); vi   = random_var()
    vh    = random_var(); vb   = random_var(); vok  = random_var()
    vsig  = random_var(); vws  = random_var(); va   = random_var()
    vbb   = random_var(); vc   = random_var(); vd   = random_var()
    vres  = random_var()

    frag_assigns = ';'.join(f"{v}={repr(bytes(enc))}" for v, enc in all_frags)
    key_reassemble = b'+'.join(
        f"bytes([b^{frag_xk[i]} for b in {v}])".encode()
        for i, v in enumerate(fv)
    ).decode()

    # Build the full decryption stub as a Python code string
    stub = (
        f"import struct;"
        f"{frag_assigns};"
        f"{vkey}={key_reassemble};"
        f"{vnon}=bytes.fromhex('{nonce_hex}');"
        f"{vctr}={ctr};"
        f"{vct}=bytes.fromhex('{ct_hex}');"
        # Rebuild keystream inline
        f"{vsig}=[0x61707865,0x3320646E,0x79622D32,0x6B206574];"
        f"{vkey}=[int.from_bytes({vkey}[i*4:i*4+4],'little') for i in range(8)];"
        f"{vnon}=[int.from_bytes({vnon}[i*4:i*4+4],'little') for i in range(3)];"
        f"def {vblk}({vst}):\n"
        f"  {vws}=list({vst})\n"
        f"  def _qr({va},{vbb},{vc},{vd}):\n"
        f"    {va}=({va}+{vbb})&0xFFFFFFFF;{vd}^={va};{vd}=(({vd}<<16)|({vd}>>16))&0xFFFFFFFF\n"
        f"    {vc}=({vc}+{vd})&0xFFFFFFFF;{vbb}^={vc};{vbb}=(({vbb}<<12)|({vbb}>>20))&0xFFFFFFFF\n"
        f"    {va}=({va}+{vbb})&0xFFFFFFFF;{vd}^={va};{vd}=(({vd}<<8)|({vd}>>24))&0xFFFFFFFF\n"
        f"    {vc}=({vc}+{vd})&0xFFFFFFFF;{vbb}^={vc};{vbb}=(({vbb}<<7)|({vbb}>>25))&0xFFFFFFFF\n"
        f"    return {va},{vbb},{vc},{vd}\n"
        f"  for _ in range(10):\n"
        f"    {vws}[0],{vws}[4],{vws}[8],{vws}[12]=_qr({vws}[0],{vws}[4],{vws}[8],{vws}[12])\n"
        f"    {vws}[1],{vws}[5],{vws}[9],{vws}[13]=_qr({vws}[1],{vws}[5],{vws}[9],{vws}[13])\n"
        f"    {vws}[2],{vws}[6],{vws}[10],{vws}[14]=_qr({vws}[2],{vws}[6],{vws}[10],{vws}[14])\n"
        f"    {vws}[3],{vws}[7],{vws}[11],{vws}[15]=_qr({vws}[3],{vws}[7],{vws}[11],{vws}[15])\n"
        f"    {vws}[0],{vws}[5],{vws}[10],{vws}[15]=_qr({vws}[0],{vws}[5],{vws}[10],{vws}[15])\n"
        f"    {vws}[1],{vws}[6],{vws}[11],{vws}[12]=_qr({vws}[1],{vws}[6],{vws}[11],{vws}[12])\n"
        f"    {vws}[2],{vws}[7],{vws}[8],{vws}[13]=_qr({vws}[2],{vws}[7],{vws}[8],{vws}[13])\n"
        f"    {vws}[3],{vws}[4],{vws}[9],{vws}[14]=_qr({vws}[3],{vws}[4],{vws}[9],{vws}[14])\n"
        f"  return [({vws}[i]+{vst}[i])&0xFFFFFFFF for i in range(16)]\n"
        f"{vks}=bytearray();"
        f"{vi}={vctr};"
        f"while len({vks})<{n}:\n"
        f"  {vst}={vsig}+{vkey}+[{vi}]+{vnon}\n"
        f"  [{vks}.extend({vw}.to_bytes(4,'little')) for {vw} in {vblk}({vst})]\n"
        f"  {vi}+=1\n"
    )
    stub = (
        f"import struct;"
        f"{frag_assigns};"
        f"{vkey}={key_reassemble};"
        f"{vnon}=bytes.fromhex('{nonce_hex}');"
        f"{vctr}={ctr};"
        f"{vct}=bytes.fromhex('{ct_hex}');"
        f"{vsig}=[0x61707865,0x3320646E,0x79622D32,0x6B206574];"
        f"{vkey}=[int.from_bytes({vkey}[i*4:i*4+4],'little') for i in range(8)];"
        f"{vnon}=[int.from_bytes({vnon}[i*4:i*4+4],'little') for i in range(3)];"
        f"def {vblk}({vst}):\n"
        f" {vws}=list({vst})\n"
        f" def _qr(a,b,c,d):\n"
        f"  a=(a+b)&0xFFFFFFFF;d^=a;d=((d<<16)|(d>>16))&0xFFFFFFFF\n"
        f"  c=(c+d)&0xFFFFFFFF;b^=c;b=((b<<12)|(b>>20))&0xFFFFFFFF\n"
        f"  a=(a+b)&0xFFFFFFFF;d^=a;d=((d<<8)|(d>>24))&0xFFFFFFFF\n"
        f"  c=(c+d)&0xFFFFFFFF;b^=c;b=((b<<7)|(b>>25))&0xFFFFFFFF\n"
        f"  return a,b,c,d\n"
        f" for _ in range(10):\n"
        f"  {vws}[0],{vws}[4],{vws}[8],{vws}[12]=_qr({vws}[0],{vws}[4],{vws}[8],{vws}[12])\n"
        f"  {vws}[1],{vws}[5],{vws}[9],{vws}[13]=_qr({vws}[1],{vws}[5],{vws}[9],{vws}[13])\n"
        f"  {vws}[2],{vws}[6],{vws}[10],{vws}[14]=_qr({vws}[2],{vws}[6],{vws}[10],{vws}[14])\n"
        f"  {vws}[3],{vws}[7],{vws}[11],{vws}[15]=_qr({vws}[3],{vws}[7],{vws}[11],{vws}[15])\n"
        f"  {vws}[0],{vws}[5],{vws}[10],{vws}[15]=_qr({vws}[0],{vws}[5],{vws}[10],{vws}[15])\n"
        f"  {vws}[1],{vws}[6],{vws}[11],{vws}[12]=_qr({vws}[1],{vws}[6],{vws}[11],{vws}[12])\n"
        f"  {vws}[2],{vws}[7],{vws}[8],{vws}[13]=_qr({vws}[2],{vws}[7],{vws}[8],{vws}[13])\n"
        f"  {vws}[3],{vws}[4],{vws}[9],{vws}[14]=_qr({vws}[3],{vws}[4],{vws}[9],{vws}[14])\n"
        f" return [({vws}[i]+{vst}[i])&0xFFFFFFFF for i in range(16)]\n"
        f"{vks}=bytearray()\n"
        f"{vi}={vctr}\n"
        f"while len({vks})<{n}:\n"
        f" {vst}={vsig}+{vkey}+[{vi}]+{vnon}\n"
        f" [{vks}.extend({vw}.to_bytes(4,'little')) for {vw} in {vblk}({vst})]\n"
        f" {vi}+=1\n"
        f"{vh}=0\n"
        f"for {vb} in {vct}:\n"
        f" {vh}=({vh}*{BASE}+{vb})%{PRIME}\n"
        f"{vok}={vh}=={h}\n"
        f"{vres}=bytes([{vct}[{vi}]^{vks}[{vi}] for {vi} in range({n})]) if {vok} else b''\n"
        f"exec({vres}.decode()) if {vok} else None\n"
    )
    return stub

# ─────────────────────────────────────────────────────────────────────────────
# LAYER 7 — XTEA block cipher + key derived by manual SHA3-like sponge
#           + PKCS7 padding + Double XOR tweak + Custom Base91 encoding
#
#   1) 128-bit key derivation via a simplified Keccak-like sponge:
#      absorbs a 256-bit seed and squeezes 16 bytes of key material.
#   2) PKCS7 padding to the next 8-byte boundary.
#   3) XTEA encryption (64 rounds, CBC mode with random IV).
#   4) Double XOR tweak: first tweak is 32 random bytes, second derived
#      from the first via rotation and mixing — inter-dependency that
#      blocks meet-in-the-middle attacks on the tweak layer.
#   5) Custom Base91 encoding (91 printable chars, no single-quote or
#      backslash) to avoid recognizable base64 patterns.
# ─────────────────────────────────────────────────────────────────────────────
def layer7_xtea_sponge_b91(code_string):
    data = code_string.encode()

    # ── Sponge key derivation (simplified Keccak-like absorb/squeeze) ──────────
    seed_words = [random.randint(0, 0xFFFFFFFF) for _ in range(8)]

    def sponge_mix(state):
        for r in range(12):
            # theta-like: XOR columns
            C = [state[i] ^ state[i+4] ^ state[i+8] ^ state[i+12] ^ state[i+16]
                 if i < 4 else 0 for i in range(4)]
            C = [state[i%4] ^ state[4+i%4] ^ state[8+i%4] ^ state[12+i%4] ^ state[16+i%4]
                 for i in range(4)]
            for idx in range(20):
                state[idx] ^= C[idx % 4]
            # rho-like: rotate
            rots = [1,3,6,10,15,21,28,4,13,23,2,14,27,9,24,8,25,11,30,18]
            state = [((state[i] << rots[i]) | (state[i] >> (32-rots[i]))) & 0xFFFFFFFF
                     for i in range(20)]
            # pi-like: permute
            perm = [0,13,6,19,12,5,18,11,4,17,10,3,16,9,2,15,8,1,14,7]
            state = [state[perm[i]] for i in range(20)]
        return state

    sp_state = seed_words + [0]*12
    sp_state = sponge_mix(sp_state)
    key128 = []
    for w in sp_state[:4]:
        key128 += list(w.to_bytes(4, 'little'))

    key32 = [int.from_bytes(bytes(key128[i*4:i*4+4]), 'little') for i in range(4)]

    # ── PKCS7 padding ──────────────────────────────────────────────────────────
    pad_len = 8 - (len(data) % 8)
    padded  = data + bytes([pad_len] * pad_len)
    orig_data_len = len(data)

    # ── XTEA CBC encryption ────────────────────────────────────────────────────
    DELTA    = 0x9E3779B9
    N_ROUNDS = 64

    def xtea_encipher(v0, v1, key32):
        s = 0
        for _ in range(N_ROUNDS):
            v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + key32[s & 3]))) & 0xFFFFFFFF
            s  = (s + DELTA) & 0xFFFFFFFF
            v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + key32[(s >> 11) & 3]))) & 0xFFFFFFFF
        return v0, v1

    iv = [random.randint(0, 0xFFFFFFFF), random.randint(0, 0xFFFFFFFF)]
    ciphertext = bytearray()
    prev0, prev1 = iv[0], iv[1]
    for i in range(0, len(padded), 8):
        block = padded[i:i+8]
        b0 = int.from_bytes(block[:4], 'little') ^ prev0
        b1 = int.from_bytes(block[4:], 'little') ^ prev1
        e0, e1 = xtea_encipher(b0, b1, key32)
        ciphertext += e0.to_bytes(4, 'little') + e1.to_bytes(4, 'little')
        prev0, prev1 = e0, e1

    ct = bytes(ciphertext)

    # ── Double XOR tweak with inter-dependency ───────────────────────────────────
    tweak1 = bytes([random.randint(0, 255) for _ in range(32)])
    tweak2 = bytes([((tweak1[i] << 3) | (tweak1[i] >> 5)) & 0xFF ^ tweak1[(i+7)%32]
                    for i in range(32)])
    after_t1 = bytes([ct[i] ^ tweak1[i % 32] for i in range(len(ct))])
    after_t2 = bytes([after_t1[i] ^ tweak2[i % 32] for i in range(len(after_t1))])

    # ── Base91 custom encoding ─────────────────────────────────────────────────
    B91_CHARS = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        '0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~" '
    )[:91]

    def b91_encode(data):
        b = 0; n = 0; o = []
        for byte in data:
            b |= byte << n
            n += 8
            if n > 13:
                v = b & 8191
                if v > 88:
                    b >>= 13; n -= 13
                else:
                    v = b & 16383; b >>= 14; n -= 14
                o.append(B91_CHARS[v % 91])
                o.append(B91_CHARS[v // 91])
        if n:
            o.append(B91_CHARS[b % 91])
            if n > 7 or b > 90:
                o.append(B91_CHARS[b // 91])
        return ''.join(o)

    encoded = b91_encode(after_t2)

    # ── Decryption stub ───────────────────────────────────────────────────────
    seed_str  = ','.join(str(w) for w in seed_words)
    key32_str = ','.join(str(w) for w in key32)
    iv_str    = ','.join(str(w) for w in iv)
    tw1_str   = ','.join(str(b) for b in tweak1)
    tw2_str   = ','.join(str(b) for b in tweak2)

    venc  = random_var(); vkey  = random_var(); viv   = random_var()
    vtw1  = random_var(); vtw2  = random_var(); vct   = random_var()
    vat1  = random_var(); vat2  = random_var(); vblk  = random_var()
    vprev = random_var(); vi    = random_var(); vv0   = random_var()
    vv1   = random_var(); vS    = random_var(); vdelta= random_var()
    vres  = random_var(); vpad  = random_var(); vb91c = random_var()
    vb    = random_var(); vn_v  = random_var(); vo    = random_var()
    vbyte = random_var(); vv    = random_var(); vout  = random_var()

    b91_repr = repr(B91_CHARS)

    stub = (
        f"{vb91c}={b91_repr}\n"
        f"def _b91d(s):\n"
        f" v=-1;b=0;n=0;o=bytearray()\n"
        f" for c in s:\n"
        f"  p={vb91c}.find(c)\n"
        f"  if p==-1:continue\n"
        f"  if v<0:v=p\n"
        f"  else:\n"
        f"   v+=p*91;b|=v<<n;n+=13 if(v&8191)>88 else 14;v=-1\n"
        f"   while n>7:o.append(b&255);b>>=8;n-=8\n"
        f" if v>-1:o.append((b|v<<n)&255)\n"
        f" return bytes(o)\n"
        f"{venc}=_b91d({repr(encoded)})\n"
        f"{vtw1}=bytes([{tw1_str}])\n"
        f"{vtw2}=bytes([{tw2_str}])\n"
        f"{vat1}=bytes([{venc}[i]^{vtw2}[i%32] for i in range(len({venc}))])\n"
        f"{vct}=bytes([{vat1}[i]^{vtw1}[i%32] for i in range(len({vat1}))])\n"
        f"{vkey}=[{key32_str}]\n"
        f"{viv}=[{iv_str}]\n"
        f"{vdelta}=0x9E3779B9\n"
        f"def _xtea_dec(v0,v1,k):\n"
        f" s=({vdelta}*64)&0xFFFFFFFF\n"
        f" for _ in range(64):\n"
        f"  v1=(v1-(((v0<<4^v0>>5)+v0)^(s+k[(s>>11)&3])))&0xFFFFFFFF\n"
        f"  s=(s-{vdelta})&0xFFFFFFFF\n"
        f"  v0=(v0-(((v1<<4^v1>>5)+v1)^(s+k[s&3])))&0xFFFFFFFF\n"
        f" return v0,v1\n"
        f"{vres}=bytearray()\n"
        f"{vprev}=[{viv}[0],{viv}[1]]\n"
        f"for {vi} in range(0,len({vct}),8):\n"
        f" {vblk}={vct}[{vi}:{vi}+8]\n"
        f" {vv0}=int.from_bytes({vblk}[:4],'little')\n"
        f" {vv1}=int.from_bytes({vblk}[4:],'little')\n"
        f" d0,d1=_xtea_dec({vv0},{vv1},{vkey})\n"
        f" {vres}+=((d0^{vprev}[0])&0xFFFFFFFF).to_bytes(4,'little')\n"
        f" {vres}+=((d1^{vprev}[1])&0xFFFFFFFF).to_bytes(4,'little')\n"
        f" {vprev}=[{vv0},{vv1}]\n"
        f"{vpad}={vres}[-1]\n"
        f"{vout}=bytes({vres}[:{orig_data_len}])\n"
        f"exec({vout}.decode())\n"
    )
    return stub

# ─────────────────────────────────────────────────────────────────────────────
# MINI-VM — Basic stack-based virtual machine with 16 opcodes
#
#   The innermost Python stub is "compiled" to VM bytecode.
#   The VM has: a data stack, 256-slot memory, a program counter,
#   a handler table, and CALL/RET support. Each VM instruction is
#   encoded in 3 bytes: [opcode, arg_hi, arg_lo]. The interpreter
#   is emitted as Python code with randomized variable names.
#
#   Opcodes:
#     0x00 NOP          — no operation
#     0x01 PUSH imm16   — push immediate 16-bit value onto stack
#     0x02 POP          — discard top of stack
#     0x03 LOAD addr8   — load mem[addr] onto stack
#     0x04 STORE addr8  — store stack[-1] into mem[addr], pop
#     0x05 ADD          — stack[-2] += stack[-1], pop
#     0x06 XOR          — stack[-2] ^= stack[-1], pop
#     0x07 ROT r        — rotate stack[-1] left by r bits (8-bit)
#     0x08 JMP off16    — jump to absolute offset
#     0x09 JZ  off16    — jump if stack[-1]==0, pop
#     0x0A CALL off16   — push (PC+3), JMP
#     0x0B RET          — pop PC from call-stack
#     0x0C EMIT         — pop byte from stack, append to output buffer
#     0x0D EXEC         — exec(output_buffer.decode())
#     0x0E PUSH_STR idx — push byte from string-pool[idx]
#     0x0F HALT         — stop the VM
#
#   The compiler emits a PUSH/EMIT sequence for each byte of the payload,
#   interleaving NOPs, short JMPs, and inert opaque-predicate operations
#   to confuse static analysis of the bytecode.
# ─────────────────────────────────────────────────────────────────────────────
NOP   = 0x00; PUSH  = 0x01; POP   = 0x02; LOAD  = 0x03
STORE = 0x04; ADD   = 0x05; XOR_O = 0x06; ROT   = 0x07
JMP   = 0x08; JZ    = 0x09; CALL  = 0x0A; RET   = 0x0B
EMIT  = 0x0C; EXEC  = 0x0D; PHSTR = 0x0E; HALT  = 0x0F

def compile_to_vm(payload_str):
    payload = payload_str.encode()
    bc = bytearray()

    def emit3(op, hi=0, lo=0):
        nonlocal bc
        bc += bytes([op, hi, lo])

    # Opaque predicate: (x*x - x) % 2 == 0 is always True.
    # Uses ADD+XOR to emit inert noise using only available opcodes:
    # PUSH v, PUSH 0, XOR (result = v), STORE tmp, LOAD tmp, POP → net no-op.
    def opaque_nop(tmp_slot=0xFE):
        v = random.randint(1, 255)
        emit3(PUSH, 0, v)
        emit3(PUSH, 0, 0)
        emit3(XOR_O, 0, 0)
        emit3(STORE, 0, tmp_slot)
        emit3(LOAD,  0, tmp_slot)
        emit3(POP,   0, 0)

    # Fake JMP that goes nowhere new (jumps forward 3 bytes = continues normally)
    def fake_jmp():
        target = len(bc) + 6  # position right after the JMP instruction (3 bytes)
        emit3(JMP, (target >> 8) & 0xFF, target & 0xFF)

    for byte_val in payload:
        # 8% chance to insert an opaque no-op
        if random.random() < 0.08:
            opaque_nop()
        # 6% chance to insert a fake JMP
        if random.random() < 0.06:
            fake_jmp()
        emit3(PUSH, 0, byte_val)
        emit3(EMIT, 0, 0)

    emit3(EXEC, 0, 0)
    emit3(HALT, 0, 0)
    return bytes(bc)

def wrap_with_vm(payload_str):
    # Design: the large payload lives OUTSIDE the VM as a normal Python variable.
    # The VM's bytecode only encodes a tiny bootstrap stub (~100 chars) that
    # references the payload variable by name. This keeps bc_hex small regardless
    # of payload size.
    import zlib as _zlib, base64 as _b64

    compressed_payload = _zlib.compress(payload_str.encode(), 9)
    pl_b64 = _b64.b64encode(compressed_payload).decode()

    # XOR-obfuscate the b64 payload
    pl_key = random.randint(1, 127)
    pl_enc = bytes([b ^ pl_key for b in pl_b64.encode()])
    pl_hex = pl_enc.hex()

    # The payload variable name — referenced by the tiny bootstrap
    vpl_name = random_var()

    # Tiny bootstrap (no large strings) — ~100 chars
    vdec = random_var()
    bootstrap = (
        f"import zlib,base64;"
        f"{vdec}=bytes([b^{pl_key} for b in bytes.fromhex({vpl_name})]);"
        f"exec(zlib.decompress(base64.b64decode({vdec})).decode())"
    )

    # Compile tiny bootstrap to VM bytecode (bc_hex will be ~600 chars)
    bytecode = compile_to_vm(bootstrap)
    bc_hex   = bytecode.hex()

    vbc  = random_var(); vpc  = random_var(); vstk = random_var()
    vmem = random_var(); vcls = random_var(); vout = random_var()
    vop  = random_var(); vhi  = random_var(); vlo  = random_var()
    varg = random_var(); vtmp = random_var()
    v_b  = random_var()

    vm_code = (
        f"import zlib,base64\n"
        # Payload stored efficiently as a plain hex string — NOT inside bytecode
        f"{vpl_name}='{pl_hex}'\n"
        f"{vbc}=bytes.fromhex('{bc_hex}')\n"
        f"{vpc}=[0]\n"
        f"{vstk}=[]\n"
        f"{vmem}=[0]*256\n"
        f"{vcls}=[]\n"
        f"{vout}=bytearray()\n"
        f"while True:\n"
        f" {vop}={vbc}[{vpc}[0]]\n"
        f" {vhi}={vbc}[{vpc}[0]+1]\n"
        f" {vlo}={vbc}[{vpc}[0]+2]\n"
        f" {varg}=({vhi}<<8)|{vlo}\n"
        f" {vpc}[0]+=3\n"
        f" if {vop}==0x00:pass\n"
        f" elif {vop}==0x01:{vstk}.append({varg})\n"
        f" elif {vop}==0x02:{vstk}.pop()\n"
        f" elif {vop}==0x03:{vstk}.append({vmem}[{vlo}])\n"
        f" elif {vop}==0x04:{vmem}[{vlo}]={vstk}.pop()\n"
        f" elif {vop}==0x05:\n"
        f"  {vtmp}={vstk}.pop();{vstk}[-1]=({vstk}[-1]+{vtmp})&0xFF\n"
        f" elif {vop}==0x06:\n"
        f"  {vtmp}={vstk}.pop();{vstk}[-1]={vstk}[-1]^{vtmp}\n"
        f" elif {vop}==0x07:\n"
        f"  {v_b}={vstk}.pop();{vstk}.append((({v_b}<<({vlo}&7))|({v_b}>>((8-{vlo})&7)))&0xFF)\n"
        f" elif {vop}==0x08:{vpc}[0]={varg}\n"
        f" elif {vop}==0x09:\n"
        f"  {vtmp}={vstk}.pop()\n"
        f"  if {vtmp}==0:{vpc}[0]={varg}\n"
        f" elif {vop}==0x0A:{vcls}.append({vpc}[0]);{vpc}[0]={varg}\n"
        f" elif {vop}==0x0B:{vpc}[0]={vcls}.pop()\n"
        f" elif {vop}==0x0C:{vout}.append({vstk}.pop()&0xFF)\n"
        f" elif {vop}==0x0D:exec({vout}.decode());break\n"
        f" elif {vop}==0x0F:break\n"
    )
    return vm_code

# ─────────────────────────────────────────────────────────────────────────────
# ANTI-VM CHECKS
# ─────────────────────────────────────────────────────────────────────────────

ANTI_VM_WINDOWS = '''
import sys,os,platform
if platform.system()=="Windows":
    _avm_ok=True
    try:
        import winreg
        _vm_keys=[
            (winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\\VMware, Inc.\\VMware Tools"),
            (winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\\Oracle\\VirtualBox Guest Additions"),
            (winreg.HKEY_LOCAL_MACHINE,r"SYSTEM\\CurrentControlSet\\Services\\VBoxGuest"),
            (winreg.HKEY_LOCAL_MACHINE,r"HARDWARE\\ACPI\\DSDT\\VBOX__"),
            (winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\\Microsoft\\Virtual Machine\\Guest\\Parameters"),
        ]
        for _hive,_path in _vm_keys:
            try:
                _k=winreg.OpenKey(_hive,_path)
                winreg.CloseKey(_k)
                _avm_ok=False;break
            except OSError:
                pass
    except Exception:
        pass
    if not _avm_ok:
        import time;time.sleep(99999)
    try:
        import subprocess,ctypes
        _procs=subprocess.check_output("tasklist",shell=True,stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        _vm_procs=["vmtoolsd","vmwaretray","vboxservice","vboxtray","prl_tools","xenservice"]
        if any(p in _procs for p in _vm_procs):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        _dm=platform.node().lower()
        if any(x in _dm for x in ["vmware","vbox","virtual","xen","qemu"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _wmic=subprocess.check_output("wmic computersystem get model",shell=True,stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _wmic for x in ["vmware","virtualbox","virtual machine","qemu","kvm"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import psutil
        _nics=[n.lower() for n in psutil.net_if_addrs().keys()]
        if any("vmnet" in n or "vboxnet" in n or "virbr" in n for n in _nics):
            import time;time.sleep(99999)
    except Exception:
        pass
'''

ANTI_VM_LINUX = '''
import sys,os,platform
if platform.system()=="Linux":
    _avm_ok=True
    try:
        _cpuinfo=open("/proc/cpuinfo").read().lower()
        if any(x in _cpuinfo for x in ["vmware","virtualbox","qemu","bochs","kvm","xen"]):
            _avm_ok=False
    except Exception:
        pass
    if not _avm_ok:
        import time;time.sleep(99999)
    try:
        for _dmif in ["/sys/class/dmi/id/product_name","/sys/class/dmi/id/sys_vendor","/sys/class/dmi/id/board_vendor"]:
            if os.path.exists(_dmif):
                _dmi=open(_dmif).read().lower()
                if any(x in _dmi for x in ["vmware","virtualbox","qemu","bochs","xen","kvm","innotek"]):
                    import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _mnt=subprocess.check_output(["mount"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if "vboxsf" in _mnt or "vmhgfs" in _mnt:
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _ps=subprocess.check_output(["ps","aux"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _ps for x in ["vmtoolsd","vboxd","qemu","xenstored"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        _net=open("/proc/net/dev").read().lower()
        if any(x in _net for x in ["vmnet","vboxnet","virbr","veth"]):
            import time;time.sleep(99999)
    except Exception:
        pass
'''

ANTI_VM_MAC = '''
import sys,os,platform
if platform.system()=="Darwin":
    _avm_ok=True
    try:
        import subprocess
        _io=subprocess.check_output(["ioreg","-l"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _io for x in ["vmware","virtualbox","parallels","qemu","vbox"]):
            _avm_ok=False
    except Exception:
        pass
    if not _avm_ok:
        import time;time.sleep(99999)
    try:
        import subprocess
        _sp=subprocess.check_output(["system_profiler","SPHardwareDataType"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _sp for x in ["vmware","virtualbox","parallels","qemu"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _ps=subprocess.check_output(["ps","aux"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _ps for x in ["vmware","prl_tools","virtualbox","vboxservice","qemu"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _df=subprocess.check_output(["diskutil","list"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _df for x in ["vmware","vbox","parallels"]):
            import time;time.sleep(99999)
    except Exception:
        pass
    try:
        import subprocess
        _nd=subprocess.check_output(["networksetup","-listallhardwareports"],stderr=subprocess.DEVNULL).decode(errors="ignore").lower()
        if any(x in _nd for x in ["vmnet","vboxnet","parallels"]):
            import time;time.sleep(99999)
    except Exception:
        pass
'''

ANTI_VM_COMBINED = ANTI_VM_WINDOWS + "\n" + ANTI_VM_LINUX + "\n" + ANTI_VM_MAC

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED CONTROL FLOW FLATTENING
#
#   Instead of splitting source code line by line (which would break nested
#   try/except/if blocks), CFF operates on the already-encoded byte payload:
#   1) The code is compressed with zlib and encoded in base64.
#   2) The result is split into N randomly-sized chunks.
#   3) Each chunk receives a random 32-bit state ID.
#   4) A while/if-elif dispatcher reassembles the buffer in SHUFFLED
#      execution order — visually the flow appears non-linear.
#   5) Opaque predicates in every branch guarantee block execution:
#      - P1: (x*x - x) % 2 == 0  → always True
#      - P2: (a*a + a) % 2 == 0  → always True (a*(a+1) is even)
#   6) Dead blocks (unreachable states) filled with decoy code
#      confuse static CFG analysis.
#   7) The state variable is XOR'd with a "tweak" derived from the
#      previous chunk before comparison, creating inter-state dependency.
# ─────────────────────────────────────────────────────────────────────────────
def apply_control_flow_flattening(code_string):
    # Encode the full payload
    compressed = zlib.compress(code_string.encode(), 9)
    b64_payload = base64.b64encode(compressed).decode()

    # Split into N chunks
    n_chunks = random.randint(8, 16)
    chunk_sz  = max(1, len(b64_payload) // n_chunks)
    chunks    = [b64_payload[i:i+chunk_sz] for i in range(0, len(b64_payload), chunk_sz)]
    n_chunks  = len(chunks)

    # Assign unique state IDs
    all_ids    = random.sample(range(0x1000, 0xFFFFF), n_chunks + 20)
    state_ids  = all_ids[:n_chunks]
    dead_ids   = all_ids[n_chunks:]

    # Visit order (always natural 0..n-1 so the reconstructed buffer is correct)
    exec_order = list(range(n_chunks))

    final_state = random.randint(0x100000, 0x1FFFFF)
    init_state  = state_ids[exec_order[0]]

    # Inter-state tweak: tweak[i] = simple hash of the previous chunk XOR constant
    tweak_cte = random.randint(1, 0xFF)
    tweaks = [0]
    for i in range(1, n_chunks):
        prev_chunk = chunks[exec_order[i-1]]
        h = sum(ord(c) for c in prev_chunk[:8]) & 0xFF
        tweaks.append((h ^ tweak_cte) & 0xFFFF)

    # Dispatcher variables
    vst   = random_var(); vbuf  = random_var(); vtw = random_var()
    vres  = random_var(); vdec  = random_var()

    op1_x = random.randint(2, 9999)
    op2_a = random.randint(2, 9999)
    op1 = f"({op1_x}*{op1_x}-{op1_x})%2==0"
    op2 = f"({op2_a}*{op2_a}+{op2_a})%2==0"

    dead_snippets = [
        f"{random_var()}=0",
        f"{random_var()}=''",
        f"{random_var()}=[]",
        f"{random_var()}=None",
        f"{random_var()}=b''",
    ]

    L = []
    L.append(f"import zlib as _z,base64 as _b")
    L.append(f"{vst}={init_state}")
    L.append(f"{vtw}=0")
    L.append(f"{vbuf}=''")
    L.append(f"while {vst}!={final_state}:")

    # Real blocks (in execution order)
    for rank, idx in enumerate(exec_order):
        sid      = state_ids[idx]
        tweak    = tweaks[rank]
        next_id  = state_ids[exec_order[rank+1]] if rank+1 < n_chunks else final_state
        chunk    = repr(chunks[idx])
        op       = op1 if rank % 2 == 0 else op2
        cond     = f"{vst}^{vtw}=={sid}^{tweak}" if tweak else f"{vst}=={sid}"
        L.append(f"  if {cond} and {op}:")
        L.append(f"    {vbuf}+={chunk}")
        L.append(f"    {vtw}={tweak}")
        L.append(f"    {vst}={next_id}")

    # Decoy dead blocks (never reached — condition is always False)
    for did in dead_ids:
        snip = random.choice(dead_snippets)
        op   = op1 if random.random() < 0.5 else op2
        L.append(f"  elif {vst}=={did} and not({op}):")
        L.append(f"    {snip}")
        L.append(f"    {vst}={final_state}")

    L.append(f"  else: {vst}={final_state}")

    # Decode and execute
    L.append(f"{vres}=_z.decompress(_b.b64decode({vbuf}))")
    L.append(f"exec({vres}.decode())")

    return '\n'.join(L)

# ─────────────────────────────────────────────────────────────────────────────
# ADVANCED POLYMORPHISM ENGINE
#
#   Unlike the crypto layers (which encrypt data deterministically), the
#   polymorphism engine mutates the VISIBLE CODE STRUCTURE on every run so
#   that static signatures and pattern matchers cannot identify the obfuscator
#   from file layout alone. Techniques applied on each invocation:
#
#   1. Arithmetic constant encoding  — every integer literal in the generated
#      stub is replaced with a random but semantically equivalent expression:
#      XOR pair, add/sub offset, mul/div by prime, hex literal, str→int.
#   2. Key derivation chain  — the XOR decryption key is recomputed through
#      a 2-4 step arithmetic chain of random intermediate variables instead
#      of being stored as a plain literal.
#   3. Dead code injection  — a random preamble of junk classes, functions,
#      lambdas, try/except blocks, and variable assignments is inserted and
#      never executed.
#   4. Structural decryptor mutation  — 4 templates rotate randomly per run:
#        (A) for-loop + bytearray.append
#        (B) list comprehension → bytes()
#        (C) map() + lambda
#        (D) list-fold via comprehension side-effect
#   5. Opaque predicate guard  — exec() is wrapped in an always-True
#      conditional (7 variants: x(x-1)%2, x^0, isinstance, x//1, etc.).
#   6. Hex payload splitting  — the encrypted payload hex string is randomly
#      split into 2 concatenated fragments to defeat string-literal scanners.
#   7. Variable aliasing chains  — intermediate results are re-bound through
#      1-2 extra random variable names before use.
# ─────────────────────────────────────────────────────────────────────────────

def _poly_encode_int(n, _depth=0):
    """Return a Python expression string that evaluates to integer n."""
    if _depth > 1 or n < 0:
        return str(n)
    strategy = random.randint(0, 5)
    try:
        if strategy == 0:
            return f"0x{n & 0xFFFFFFFF:X}"
        elif strategy == 1:
            r = random.randint(1, 127)
            return f"({n + r}-{r})"
        elif strategy == 2:
            p = random.choice([3, 5, 7, 11, 13])
            return f"({n * p}//{p})"
        elif strategy == 3:
            xk = random.randint(1, 0xFE)
            return f"({n ^ xk}^0x{xk:X})"
        elif strategy == 4:
            return f"int('{n:x}',16)"
        else:
            return f"(lambda:({n}))()"
    except Exception:
        return str(n)


def _poly_opaque_true():
    """Return a Python expression that always evaluates to True."""
    x = random.randint(100, 9999)
    variants = [
        f"({x}*{x}-{x})%2==0",
        f"({x}*{x}+{x})%2==0",
        f"({x}^0=={x})",
        f"({x}//1=={x})",
        f"isinstance({x},int)",
        f"bool({x}|1)",
        f"len(str({x}))>0",
    ]
    return random.choice(variants)


def _poly_junk_line():
    """Return one syntactically valid line of dead code."""
    vn = random_var()
    kind = random.randint(0, 9)
    if kind == 0:
        return f"{vn} = None"
    elif kind == 1:
        return f"{vn} = lambda *_a, **_k: None"
    elif kind == 2:
        return f"{vn} = {_poly_encode_int(random.randint(0, 0xFFFF))}"
    elif kind == 3:
        return f"{vn} = [None for _ in range(0)]"
    elif kind == 4:
        return f"{vn} = getattr(object, '__doc__', None)"
    elif kind == 5:
        tag = random_var(4)
        return f"{vn} = type('_{tag}', (), {{}})()"
    elif kind == 6:
        return f"{vn} = {{k: None for k in []}}"
    elif kind == 7:
        v2 = random_var()
        val = _poly_encode_int(random.randint(1, 99))
        return (f"try:\n    {vn} = {val}\nexcept Exception:\n    {v2} = None")
    elif kind == 8:
        return f"{vn} = (lambda: None)()"
    else:
        return f"{vn} = bytes()"


def _poly_junk_function():
    """Return a dead function definition (defined but never called)."""
    fname = random_var()
    arg   = random_var(4)
    bvar  = random_var()
    inner = _poly_encode_int(random.randint(0, 0xFF))
    return (
        f"def {fname}(*{arg}):\n"
        f"    {bvar} = {arg}[0] if {arg} else {inner}\n"
        f"    return {bvar}"
    )


def _poly_junk_class():
    """Return a dead class definition (never instantiated)."""
    cname = random_var()
    attr  = random_var(4)
    val   = _poly_encode_int(random.randint(0, 0xFFFF))
    return (
        f"class {cname}:\n"
        f"    {attr} = {val}\n"
        f"    def __init__(self): pass"
    )


def _poly_preamble():
    """Build a shuffled preamble of dead-code blocks."""
    blocks = []
    for _ in range(random.randint(3, 7)):
        blocks.append(_poly_junk_line())
    for _ in range(random.randint(1, 3)):
        blocks.append(_poly_junk_function())
    for _ in range(random.randint(0, 2)):
        blocks.append(_poly_junk_class())
    random.shuffle(blocks)
    return "\n".join(blocks)


def _poly_key_chain(key):
    """
    Return (setup_lines, key_var_name) where setup_lines is Python code
    that defines key_var_name = key via a 2-4 step arithmetic chain,
    hiding the raw key value behind intermediate random variables.
    """
    steps   = random.randint(2, 4)
    offsets = [random.randint(1, 127) for _ in range(steps - 1)]

    # Build the cumulative value: key + sum(offsets) stored as final
    cumulative = key
    intermediates = []
    for r in offsets:
        cumulative = (cumulative + r) % 256
        intermediates.append(cumulative)

    # Emit code that starts from the cumulative value and subtracts back
    lines = []
    v = random_var()
    lines.append(f"{v} = {_poly_encode_int(intermediates[-1])}")
    for r in reversed(offsets):
        nv = random_var()
        lines.append(f"{nv} = ({v}-{_poly_encode_int(r)})%{_poly_encode_int(256)}")
        v = nv

    return "\n".join(lines), v


def apply_advanced_polymorphism(code_string):
    """
    Wrap code_string in a structurally unique polymorphic shell.
    Every call produces a structurally different Python file:
      - Compress + XOR-encrypt the payload with a random key.
      - Decode via one of 4 structural templates.
      - Hide the key behind a multi-step arithmetic chain.
      - Inject a dead-code preamble (classes, functions, lambdas).
      - Guard exec() with an opaque always-True predicate.
      - Optionally split the hex payload string in two.
    """
    # Compress + XOR-encrypt
    compressed = zlib.compress(code_string.encode(), 9)
    key        = random.randint(1, 254)
    encrypted  = bytes([b ^ key for b in compressed])
    hex_enc    = encrypted.hex()

    # Fresh random variable names
    vdata = random_var(); vout  = random_var()
    vi    = random_var(); vbuf  = random_var()
    vzlib = random_var(); vk    = random_var()

    opaque = _poly_opaque_true()

    # Key expression — sometimes a plain encoded int, sometimes a full chain
    if random.random() < 0.6:
        key_setup, key_expr = _poly_key_chain(key)
    else:
        key_setup = ""
        key_expr  = _poly_encode_int(key)

    # Hex string — optionally split into two concatenated string literals
    if random.random() < 0.45 and len(hex_enc) > 20:
        mid      = (random.randint(len(hex_enc) // 3, 2 * len(hex_enc) // 3)) & ~1
        hex_expr = f"('{hex_enc[:mid]}'+'{hex_enc[mid:]}')"
    else:
        hex_expr = f"'{hex_enc}'"

    # Alias chain: vdata → alias1 (→ alias2 with 40% chance)
    alias1 = random_var()
    use_alias2 = random.random() < 0.4
    alias2 = random_var()
    alias_setup  = f"{alias1}=bytes.fromhex({hex_expr})\n"
    alias_setup += f"{alias2}={alias1}\n" if use_alias2 else ""
    final_data   = alias2 if use_alias2 else alias1

    # Choose structural decryptor template
    t = random.randint(0, 3)

    if t == 0:
        # Template A — for-loop + bytearray.append
        decryptor = (
            f"import zlib as {vzlib}\n"
            f"{key_setup + chr(10) if key_setup else ''}"
            f"{alias_setup}"
            f"{vout}=bytearray()\n"
            f"for {vi} in {final_data}:{vout}.append({vi}^{key_expr})\n"
            f"exec({vzlib}.decompress(bytes({vout})).decode()) if {opaque} else None"
        )
    elif t == 1:
        # Template B — list comprehension → bytes()
        decryptor = (
            f"import zlib as {vzlib}\n"
            f"{key_setup + chr(10) if key_setup else ''}"
            f"{alias_setup}"
            f"{vout}=bytes([{vi}^{key_expr} for {vi} in {final_data}])\n"
            f"exec({vzlib}.decompress({vout}).decode()) if {opaque} else None"
        )
    elif t == 2:
        # Template C — map() + lambda
        decryptor = (
            f"import zlib as {vzlib}\n"
            f"{key_setup + chr(10) if key_setup else ''}"
            f"{vk}={key_expr}\n"
            f"{alias_setup}"
            f"{vout}=bytes(map(lambda _b:_b^{vk},{final_data}))\n"
            f"exec({vzlib}.decompress({vout}).decode()) if {opaque} else None"
        )
    else:
        # Template D — list-fold via comprehension side-effect
        decryptor = (
            f"import zlib as {vzlib}\n"
            f"{key_setup + chr(10) if key_setup else ''}"
            f"{alias_setup}"
            f"{vbuf}=[]\n"
            f"[{vbuf}.append(_x^{key_expr}) for _x in {final_data}]\n"
            f"{vout}=bytes({vbuf})\n"
            f"exec({vzlib}.decompress({vout}).decode()) if {opaque} else None"
        )

    # Strip stray blank lines introduced by empty key_setup
    decryptor = "\n".join(ln for ln in decryptor.split("\n") if ln.strip())

    preamble = _poly_preamble()
    return preamble + "\n" + decryptor


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────
def obfuscate(source_code):
    repeat_label = variable_names.strip() if variable_names.strip() else "__Encrypted__"

    # Pipeline order: heavy crypto layers (6 & 7) run on compact payloads
    # (layers 1-4 compress heavily via zlib). The visual layer (5) runs last
    # so its massive expansion is never seen by ChaCha20 or XTEA.

    print(f"{ORANGE}  [*] Injecting anti-VM checks (Windows + Linux + macOS)...{RESET}")
    source_with_avm = ANTI_VM_COMBINED + "\n" + source_code

    print(f"{ORANGE}  [*] Applying advanced Control Flow Flattening...{RESET}")
    source_flattened = apply_control_flow_flattening(source_with_avm)

    print(f"{RED}  [*] Layer 1 — Marshal + Chaotic maps (logistic/tent/circle) + Fibonacci seeds + Base85{RESET}")
    result = layer1_marshal_logistic_b85(source_flattened)

    print(f"{RED}  [*] Layer 2 — Zlib + Dual random Base64 alphabets + Bit rotation + XOR + Nibble swap{RESET}")
    result = layer2_custom_b64_bitrot(result)

    print(f"{RED}  [*] Layer 3 — Sub256 + Vigenere + Double columnar transposition + RC4 stream + Hex{RESET}")
    result = layer3_sub_vig_transpose_hex(result)

    print(f"{RED}  [*] Layer 4 — Base85 + Zlib + Chained XOR fragments + decoy keys{RESET}")
    result = layer4_decoy_xor_fragments(result)

    print(f"{RED}  [*] Layer 6 — ChaCha20-ARX quarter-round + Polynomial integrity hash + key fragments{RESET}")
    result = layer6_chacha_arx_integrity(result)

    print(f"{RED}  [*] Layer 7 — XTEA-CBC 64 rounds + Sponge KDF + Double XOR tweak + Custom Base91{RESET}")
    result = layer7_xtea_sponge_b91(result)

    print(f"{ORANGE}  [*] Wrapping in stack-based Mini-VM (opaque predicates + fake NOPs + fake JMPs)...{RESET}")
    result = wrap_with_vm(result)

    # Polymorphism runs after the VM so its structural mutations are encrypted
    # by Layer 5. Every invocation produces a structurally unique outer shell.
    print(f"{ORANGE}  [*] Applying advanced polymorphic mutations (template, dead code, key chain, opaque predicates)...{RESET}")
    result = apply_advanced_polymorphism(result)

    # Layer 5 (visual) runs last — its massive expansion stays at the outermost
    # shell so the inner crypto layers never process the padded output.
    print(f"{ORANGE}  [*] Layer 5 (outer visual shell) — Dual LCG + XOR + Visual noise '{repeat_label}'...{RESET}")
    result = layer5_encrypted_visual(result)

    print(f"\n{BOLD}{ORANGE}  [+] 7-layer obfuscation + Mini-VM + Polymorphism complete!{RESET}")
    return result

# ─────────────────────────────────────────────────────────────────────────────
# BANNER & MENU
# ─────────────────────────────────────────────────────────────────────────────

ASCII_BANNER = r"""
 ██╗██████╗ ██████╗ ███████╗
███║╚════██╗╚════██╗╚════██║
╚██║ █████╔╝ █████╔╝    ██╔╝
 ██║ ╚═══██╗ ╚═══██╗   ██╔╝ 
 ██║██████╔╝██████╔╝   ██║  
 ╚═╝╚═════╝ ╚═════╝    ╚═╝  
"""

def _gradient_banner(text):
    """Print the ASCII banner with a blood-red → orange gradient line by line."""
    lines = text.split("\n")
    # 6 visible lines: transition from blood-red to orange
    colors = [
        "\033[38;2;160;0;0m",
        "\033[38;2;190;20;0m",
        "\033[38;2;215;55;0m",
        "\033[38;2;235;90;0m",
        "\033[38;2;250;125;0m",
        "\033[38;2;255;150;0m",
    ]
    visible = [l for l in lines if l.strip()]
    ci = 0
    for line in lines:
        if line.strip():
            c = colors[min(ci, len(colors) - 1)]
            print(f"{BOLD}{c}{line}{RESET}")
            ci += 1
        else:
            print()

def _r(text):
    """Blood-red styled text."""
    return f"{BOLD}{RED}{text}{RESET}"

def _o(text):
    """Orange styled text."""
    return f"{BOLD}{ORANGE}{text}{RESET}"

def _dim(text):
    """Dimmed text for secondary info."""
    return f"{DIM}{text}{RESET}"

def print_menu():
    """Print the full startup menu."""
    _gradient_banner(ASCII_BANNER)

    W = 68
    border_top    = f"{BOLD}{RED}╔{'═' * W}╗{RESET}"
    border_bot    = f"{BOLD}{RED}╚{'═' * W}╝{RESET}"
    border_mid    = f"{BOLD}{RED}╠{'═' * W}╣{RESET}"
    def row(text="", color=None):
        inner = text if color is None else f"{color}{text}{RESET}"
        # strip ANSI for length calculation
        import re
        plain = re.sub(r'\033\[[0-9;]*m', '', inner)
        pad = W - len(plain)
        print(f"{BOLD}{RED}║{RESET} {inner}{' ' * (pad - 1)}{BOLD}{RED}║{RESET}")

    print(border_top)
    row()
    row("  ADVANCED PYTHON OBFUSCATOR  —  7 LAYERS + MINI-VM", ORANGE)
    row("  Anti-VM  ·  Control Flow Flattening  ·  Max Level", RED)
    row()
    print(border_mid)
    row()
    row("  ENCRYPTION LAYERS", ORANGE)
    row()
    row("  01  Marshal + 3 Chaotic maps (logistic/tent/circle)", RED)
    row("      Fibonacci seeds · CBC feedback · Base85", _dim(""))
    row()
    row("  02  Zlib + Dual random Base64 alphabets", RED)
    row("      Bit rotation · Positional XOR · Nibble swap", _dim(""))
    row()
    row("  03  Sub256 + Vigenere (32-64 key) + RC4 stream", RED)
    row("      Double columnar transposition · Hex encoding", _dim(""))
    row()
    row("  04  Base85 + Zlib + Chained XOR fragments", RED)
    row("      10-16 decoy fragments with fake keys", _dim(""))
    row()
    row("  05  Dual LCG (2 seeds) + XOR · Visual noise shell", RED)
    row()
    row("  06  ChaCha20-ARX quarter-round keystream", RED)
    row("      Polynomial integrity hash · Key fragment decoys", _dim(""))
    row()
    row("  07  XTEA-CBC 64 rounds + Sponge KDF", RED)
    row("      Double XOR tweak · Custom Base91 encoding", _dim(""))
    row()
    print(border_mid)
    row()
    row("  ACTIVE PROTECTIONS", ORANGE)
    row()
    row("  ►  Stack-based Mini-VM  (16 opcodes, opaque predicates,", RED)
    row("     fake NOPs, fake JMPs, bootstrap isolation)", _dim(""))
    row()
    row("  ►  Anti-VM  ·  Windows  (registry, WMI, processes,", RED)
    row("     hostname, NICs  —  5 independent checks)", _dim(""))
    row()
    row("  ►  Anti-VM  ·  Linux    (/proc/cpuinfo, DMI sysfs,", RED)
    row("     mount, ps aux, /proc/net  —  5 checks)", _dim(""))
    row()
    row("  ►  Anti-VM  ·  macOS    (ioreg, system_profiler,", RED)
    row("     ps, diskutil, networksetup  —  5 checks)", _dim(""))
    row()
    row("  ►  Control Flow Flattening  (state dispatcher, opaque", RED)
    row("     predicates, inter-state XOR tweak, dead blocks)", _dim(""))
    row()
    row("  ►  Advanced Polymorphism  (4 structural decryptor templates,", RED)
    row("     arithmetic constant encoding, key derivation chain,", _dim(""))
    row("     dead-code preamble, opaque predicate guard,", _dim(""))
    row("     hex payload splitting, variable aliasing chains)", _dim(""))
    row()
    print(border_bot)
    print()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print_menu()

    # ── Input file ────────────────────────────────────────────────────────────
    while True:
        input_file = input(
            f"{BOLD}{ORANGE}  Enter the path of the .py file to obfuscate: {RESET}"
        ).strip()
        if not input_file:
            print(f"{RED}  [!] Path cannot be empty. Try again.{RESET}")
            continue
        if not os.path.isfile(input_file):
            print(f"{RED}  [!] File not found: '{input_file}'. Try again.{RESET}")
            continue
        if not input_file.endswith('.py'):
            print(f"{ORANGE}  [!] Warning: file does not have a .py extension.{RESET}")
        break

    with open(input_file, 'r', encoding='utf-8') as f:
        source_code = f.read()

    if not source_code.strip():
        print(f"{RED}  [!] Error: file is empty.{RESET}")
        sys.exit(1)

    print(f"\n{_dim('  Source file  :')}{BOLD} {input_file}{RESET}")
    print(f"{_dim('  Source size  :')}{BOLD} {len(source_code):,} bytes{RESET}")

    # ── Output file ───────────────────────────────────────────────────────────
    default_out = os.path.splitext(input_file)[0] + "_obfuscated.py"
    out_prompt  = (
        f"{BOLD}{ORANGE}  Output filename "
        f"{_dim(f'[default: {os.path.basename(default_out)}]')}"
        f"{BOLD}{ORANGE}: {RESET}"
    )
    output_file = input(out_prompt).strip()
    if not output_file:
        output_file = default_out
    elif not output_file.endswith('.py'):
        output_file += '.py'

    # ── Run obfuscation ───────────────────────────────────────────────────────
    print(f"\n{_o('  ─' * 34)}")
    print(f"{_o('  Starting obfuscation pipeline...')}")
    print(f"{_o('  ─' * 34)}\n")

    obfuscated = obfuscate(source_code)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated)

    # ── Summary ───────────────────────────────────────────────────────────────
    ratio = len(obfuscated) / len(source_code)
    print(f"\n{BOLD}{RED}  ╔{'═' * 46}╗{RESET}")
    print(f"{BOLD}{RED}  ║{RESET}  {_o('OBFUSCATION COMPLETE')}"
          f"{' ' * 26}{BOLD}{RED}║{RESET}")
    print(f"{BOLD}{RED}  ╠{'═' * 46}╣{RESET}")
    print(f"{BOLD}{RED}  ║{RESET}  Output file  : {BOLD}{output_file:<28}{RESET}  {BOLD}{RED}║{RESET}")
    print(f"{BOLD}{RED}  ║{RESET}  Source size  : {BOLD}{len(source_code):>10,} bytes{' ' * 15}{RESET}{BOLD}{RED}║{RESET}")
    print(f"{BOLD}{RED}  ║{RESET}  Output size  : {BOLD}{len(obfuscated):>10,} bytes{' ' * 15}{RESET}{BOLD}{RED}║{RESET}")
    print(f"{BOLD}{RED}  ║{RESET}  Expansion    : {BOLD}{ratio:>10.1f}x{' ' * 19}{RESET}{BOLD}{RED}║{RESET}")
    print(f"{BOLD}{RED}  ╚{'═' * 46}╝{RESET}\n")

if __name__ == '__main__':
    main()
