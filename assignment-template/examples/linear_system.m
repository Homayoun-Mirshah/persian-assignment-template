% Solve and check a linear system.
A = [3, 1; 1, 2];
b = [9; 8];
x = A \ b;

if norm(A * x - b) < 1e-10
    disp('Solution verified');
end

fprintf('x = [%.1f, %.1f]\n', x(1), x(2));
