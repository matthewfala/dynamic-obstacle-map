
# Euler vector rotation
# Ref pg 13 https://www.cs.utexas.edu/~theshark/courses/cs354/lectures/cs354-14.pdf
def euler_vector_rotate(v, alpha, beta, gamma):
    # Rotate about alpha
    x = v.item(0)
    y = v.item(1)
    z = v.item(2)
    v_alpha = np.array([x, y * math.cos(alpha) - z * math.sin(alpha), y * math.sin(alpha) + z * math.cos(alpha)])

    # Rotate about beta
    x = v_alpha.item(0)
    y = v_alpha.item(1)
    z = v_alpha.item(2)
    v_beta = np.array([x * math.cos(beta) + z * math.sin(beta), y, -x * math.sin(beta) + y * math.cos(beta)])

    # Rotate about gamma
    x = v_beta.item(0)
    y = v_beta.item(1)
    z = v_beta.item(2)
    v_gamma = np.array([x * math.cos(gamma) - y * math.sin(gamma), x * math.sin(gamma) + y * math.cos(gamma), z])

    #return fully rotated array
    return v_gamma

