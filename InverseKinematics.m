x = csvread("x_vals.csv");
y = csvread("y_vals.csv");

% Define the length of each link
L1 = 6.25; % Length of link 1
L2 = 12; % Length of link 2

x2 = linspace(x(end),x(1),3*length(x));
y2 = linspace(y(end),y(1),3*length(y));

t = linspace(0,8*pi,length(x)*4);

x = [x',x2];
y = [y',y2];
%y = [y',y2]+sin(t)/2+1/2; % Add a bounce to the y direction motion

% Define the target point coordinates (as an array of x and y values)
%targetPoints = [x';y'];
targetPoints = [x;y];

theta2 = zeros(1,length(targetPoints));
theta1 = zeros(1,length(targetPoints));

% Loop through each target point and calculate the joint angles
for i = 1:length(targetPoints)
    X = targetPoints(1, i); % Target x-coordinate
    Y = targetPoints(2, i); % Target y-coordinate

    % Calculate the inverse kinematics
    r = sqrt(X^2 + Y^2);
    theta2(i) = acos((r^2 - L1^2 - L2^2) / (2 * L1 * L2));
    theta1(i) = atan2(Y, X) - atan2((L2 * sin(theta2(i))), (L1 + L2 * cos(theta2(i))));
end

testX = L1*cos(theta1) + L2*cos(theta1+theta2);
testY = L1*sin(theta1) + L2*sin(theta1+theta2);

subplot(3,1,1)
scatter(testX,testY)
title("X-Y coordinates")

subplot(3,1,2)
plot(theta1)
title("theta1 Values")

subplot(3,1,3)
plot(theta2)
title("theta2 Values")

theta1 = theta1 + pi/2;
%theta2 = theta2 + pi/2;

theta1 = theta1*180/pi;
theta2 = theta2*180/pi;
