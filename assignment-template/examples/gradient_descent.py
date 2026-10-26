def objective(x):
    return (x - 3.0) ** 2 + 1.0


def gradient_descent(x0=0.0, learning_rate=0.2, steps=10):
    x = x0
    for _ in range(steps):
        gradient = 2.0 * (x - 3.0)
        x -= learning_rate * gradient
    return x


if __name__ == "__main__":
    result = gradient_descent()
    print(f"x = {result:.6f}")
    print(f"f(x) = {objective(result):.6f}")
    print(f"error = {abs(result - 3.0):.6f}")
