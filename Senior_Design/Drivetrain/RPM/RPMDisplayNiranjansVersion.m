% MATLAB code to read serial data from Arduino using serialport object
% This file runs in conjunction with Arduino_Power_Code.ino

% Connect to Arduino
comPort = 'COM4';  
baudRate = 115200; % Make sure it is the same as the arduino code

% Open the serial port
serialConnect = serialport(comPort, baudRate);
configureTerminator(serialConnect, "LF"); 

% Prompt the user for the output data file name
outputFileName = input('Enter the output data file name in the format Initials_#.txt (e.g. TE_1.txt): ', 's');

% Determine test data folder and get full file path
underscoreIndex = strfind(outputFileName, '_');
outputTestFolder = outputFileName(1:underscoreIndex(1)-1);
outputFileName = "./Onland_Testing_Data/" + outputTestFolder + "/" + outputFileName;

% Create the directory if it doesn't exist
outputDirectory = fileparts(outputFileName);
if ~isfolder(outputDirectory)
    mkdir(outputDirectory);
end

% Open the data file for writing
dataFile = fopen(outputFileName, 'w');

% Check if the file was opened successfully
if dataFile == -1
    error(['Unable to open the file ', outputFileName, ' for writing.']);
end

% Duration to read data (in seconds).
duration = 120;

% Initialize arrays for storing data and timestamps.
Activations = [];
timeValues = [];

% Create a figure for real-time plotting
figure;
f = animatedline; % Sensor 1
g = animatedline; % Sensor 2
h = animatedline; % Sensor 3
title("Activations");
xlabel("Time (s)");
ylabel("Amplitude");

% Wait for space bar to be pressed
disp('Press the space bar to start collecting data.');
waitForKeyPress(' ');

tic;
while toc <= duration
    % Check if there is data available
    if serialConnect.NumBytesAvailable > 0
        % Read data from Arduino
        data = str2double(readline(serialConnect));
        
        % Store the read data in the corresponding data arrays.
        currentTime = toc;
        timeValues = [timeValues currentTime];
        Activations = [Activations data];

        % Update plot
        if data == 1
            addpoints(f, currentTime, data);
        elseif data == 2
            addpoints(g, currentTime, data);
        else
            addpoints(h, currentTime, data);
        end

        xlim([currentTime - 10, currentTime]);
        drawnow;

        % Write time value to data file if corresponding activation is 1
        if data ~= 0
            fprintf(dataFile, '%f, %d\n', currentTime, data);
        end
    end
end

% Close serial connection
clear serialConnect; % This will also close the connection

% Close the data file
fclose(dataFile);

% Calculate Quantities
revTimes = timeValues(logical([0 (diff(Activations) == 1)]));
RPM = 60 ./ diff(revTimes);

%% Plots
figure;
tiledlayout(2, 1)

% Plot Activations
nexttile
plot(timeValues, Activations);
title("Activations");
xlabel("Time (s)");
ylabel("Amplitude");

% Plot RPM
nexttile
plot(revTimes(2:end), RPM);
title("RPM");
xlabel("Time (s)");
ylabel("RPM");

%% Functions
% Function to wait for a specific key press
function waitForKeyPress(key)
    disp(['Waiting for key press (', key, ')...']);
    while true
        k = waitforbuttonpress;
        if k == 1 && strcmp(get(gcf, 'CurrentCharacter'), key)
            break;
        end
    end
    disp(['Key press detected: ', key]);
end