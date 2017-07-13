function [] = canalSurface(exercise)
% exercise = 'Swipeleft'
exercise_file = ['data/Slow' exercise 'Data.mat']
hand_file = ['data/' exercise 'HandOutputSlowTest.mat']
upper_file = ['data/' exercise 'UpperOutputSlowTest.mat']
lower_file = ['data/' exercise 'LowerOutputSlowTest.mat']
sd = load(exercise_file)
sd = sd.('data');
sd = sd';
sd(1, :)    
sd(2, :) = []
steps = sd(1,:);
sd(1,:) = sd(1,:)+1;
steps = steps + 1

max_ = max(steps)
min_ = min(steps)

demoSize = max_
totalSamples = size(steps, 2)
numDemos = 1

upper_coord = [0, 0, 0];
lower_coord = [0, 0, 0];
hand_coord = [0, 0, 0];

upper_coord_2 = [0, 0, 0];
lower_coord_2 = [0, 0, 0];
hand_coord_2 = [0, 0, 0];

upper_ang = [0, 0, 0];
lower_ang = [0, 0, 0];
hand_ang = [0, 0, 0];

upper_coord_set = {};
lower_coord_set = {};
hand_coord_set = {};

upper_ang_set = {};
lower_ang_set = {};
hand_ang_set = {};

upper_coord_set_2 = {};
lower_coord_set_2 = {};
hand_coord_set_2 = {};

max_distance_upper = -9999*ones(1, max_);
max_distance_upper_2 = -9999*ones(1, max_);
max_distance_lower = -9999*ones(1, max_);
max_distance_lower_2 = -9999*ones(1, max_);
max_distance_hand = -9999*ones(1, max_);
max_distance_hand_2 = -9999*ones(1, max_);

upper_high_x = -9999*ones(1, max_);
upper_high_y = -9999*ones(1, max_);
upper_high_z = -9999*ones(1, max_);
upper_high_x_2 = -9999*ones(1, max_);
upper_high_y_2 = -9999*ones(1, max_);
upper_high_z_2 = -9999*ones(1, max_);
lower_high_x = -9999*ones(1, max_);
lower_high_y = -9999*ones(1, max_);
lower_high_z = -9999*ones(1, max_);
lower_high_x_2 = -9999*ones(1, max_);
lower_high_y_2 = -9999*ones(1, max_);
lower_high_z_2 = -9999*ones(1, max_);
hand_high_x = -9999*ones(1, max_);
hand_high_y = -9999*ones(1, max_);
hand_high_z = -9999*ones(1, max_);
hand_high_x_2 = -9999*ones(1, max_);
hand_high_y_2 = -9999*ones(1, max_);
hand_high_z_2 = -9999*ones(1, max_);

upper_high_ang_x = -9999*ones(1, max_);
upper_high_ang_y = -9999*ones(1, max_);
upper_high_ang_z = -9999*ones(1, max_);
upper_low_ang_x = 9999*ones(1, max_);
upper_low_ang_y = 9999*ones(1, max_);
upper_low_ang_z = 9999*ones(1, max_);

lower_high_ang_x = -9999*ones(1, max_);
lower_high_ang_y = -9999*ones(1, max_);
lower_high_ang_z = -9999*ones(1, max_);
lower_low_ang_x = 9999*ones(1, max_);
lower_low_ang_y = 9999*ones(1, max_);
lower_low_ang_z = 9999*ones(1, max_);

hand_high_ang_x = -9999*ones(1, max_);
hand_high_ang_y = -9999*ones(1, max_);
hand_high_ang_z = -9999*ones(1, max_);
hand_low_ang_x = 9999*ones(1, max_);
hand_low_ang_y = 9999*ones(1, max_);
hand_low_ang_z = 9999*ones(1, max_);

upper_low_x = 9999*ones(1, max_);
upper_low_y = 9999*ones(1, max_);
upper_low_z = 9999*ones(1, max_);
upper_low_x_2 = 9999*ones(1, max_);
upper_low_y_2 = 9999*ones(1, max_);
upper_low_z_2 = 9999*ones(1, max_);
lower_low_x = 9999*ones(1, max_);
lower_low_y = 9999*ones(1, max_);
lower_low_z = 9999*ones(1, max_);
lower_low_x_2 = 9999*ones(1, max_);
lower_low_y_2 = 9999*ones(1, max_);
lower_low_z_2 = 9999*ones(1, max_);
hand_low_x = 9999*ones(1, max_);
hand_low_y = 9999*ones(1, max_);
hand_low_z = 9999*ones(1, max_);
hand_low_x_2 = 9999*ones(1, max_);
hand_low_y_2 = 9999*ones(1, max_);
hand_low_z_2 = 9999*ones(1, max_);

upper_coord_x = {};
upper_coord_y = {};
upper_coord_z = {};
upper_coord_x_2 = {};
upper_coord_y_2 = {};
upper_coord_z_2 = {};

upper_ang_x = {};
upper_ang_y = {};
upper_ang_z = {};
lower_ang_X = {};
lower_ang_y = {};
lower_ang_z = {};
hand_ang_x = {};
hand_ang_y = {};
hand_ang_z = {};

upper_ang_set = {};
lower_ang_set = {};
hand_ang_set = {};

idx = 1;
for(i = 1:demoSize)
    i
    sd(1,i)
    idx_ = mod(i, max_);
    if(idx_==0)
        idx_ = max_;
    end
    if(sd(2,i)>upper_high_x(idx_))
        upper_high_x(idx_) = sd(2, i);
    end
    if(sd(2,i)<upper_low_x(idx_))
        upper_low_x(idx_) = sd(2, i);
    end

    if(sd(3,i)>upper_high_y(idx_))
        upper_high_y(idx_) = sd(3, i);
    end
    if(sd(3,i)<upper_low_y(idx_))
        upper_low_y(idx_) = sd(3, i);
    end

    if(sd(4,i)>upper_high_z(idx_))
        upper_high_z(idx_) = sd(4, i);
    end
    if(sd(4,i)<upper_low_z(idx_))
        upper_low_z(idx_) = sd(4, i);
    end
    
    upper_coord = [upper_coord; [sd(2,i), sd(3,i) sd(4,i)]];
    lower_coord = [lower_coord; [sd(9,i), sd(10,i) sd(11,i)]];
    hand_coord = [hand_coord; [sd(16,i), sd(17,i) sd(18,i)]];
    
    upper_ang = [upper_ang; quat2eul([sd(5,i) sd(6,i) sd(7,i) sd(8,i)])];
    lower_ang = [lower_ang; quat2eul([sd(12,i) sd(13,i) sd(14,i) sd(15,i)])];
    hand_ang = [hand_ang; quat2eul([sd(19,i) sd(20,i) sd(21,i) sd(22,i)])];
    
    % idx_
    % size(upper_ang)
    % size(upper_coord)
    % size(upper_high_ang_x)
    % upper_ang(i, 1)
    % upper_high_ang_x(idx_)
    if(upper_ang(idx_, 1)>upper_high_ang_x(idx_))
        upper_high_ang_x(idx_) = upper_ang(idx_, 1);
    end
    if(upper_ang(idx_, 1)<upper_low_ang_x(idx_))
        upper_low_ang_x(idx_) = upper_ang(idx_, 1);
    end
    if(upper_ang(idx_, 2)>upper_high_ang_y(idx_))
        upper_high_ang_y(idx_) = upper_ang(idx_, 2);
    end
    if(upper_ang(idx_, 2)<upper_low_ang_y(idx_))
        upper_low_ang_y(idx_) = upper_ang(idx_, 2);
    end
    if(upper_ang(idx_, 3)>upper_high_ang_z(idx_))
        upper_high_ang_z(idx_) = upper_ang(idx_, 3);
    end
    if(upper_ang(idx_, 3)<upper_low_ang_z(idx_))
        upper_low_ang_z(idx_) = upper_ang(idx_, 3);
    end
    
    if(lower_ang(idx_, 1)>lower_high_ang_x(idx_))
        lower_high_ang_x(idx_) = lower_ang(idx_, 1);
    end
    if(lower_ang(idx_, 1)<lower_low_ang_x(idx_))
        lower_low_ang_x(idx_) = lower_ang(idx_, 1);
    end
    if(lower_ang(idx_, 2)>lower_high_ang_y(idx_))
        lower_high_ang_y(idx_) = lower_ang(idx_, 2);
    end
    if(lower_ang(idx_, 2)<lower_low_ang_y(idx_))
        lower_low_ang_y(idx_) = lower_ang(idx_, 2);
    end
    if(lower_ang(idx_, 3)>lower_high_ang_z(idx_))
        lower_high_ang_z(idx_) = lower_ang(idx_, 3);
    end
    if(lower_ang(idx_, 3)<lower_low_ang_z(idx_))
        lower_low_ang_z(idx_) = lower_ang(idx_, 3);
    end
    
    if(hand_ang(idx_, 1)>hand_high_ang_x(idx_))
        hand_high_ang_x(idx_) = hand_ang(idx_, 1);
    end
    if(hand_ang(idx_, 1)<hand_low_ang_x(idx_))
        hand_low_ang_x(idx_) = hand_ang(idx_, 1);
    end
    if(hand_ang(idx_, 2)>hand_high_ang_y(idx_));
        hand_high_ang_y(idx_) = hand_ang(idx_, 2);
    end
    if(hand_ang(idx_, 2)<hand_low_ang_y(idx_))
        hand_low_ang_y(idx_) = hand_ang(idx_, 2);
    end
    if(hand_ang(idx_, 3)>hand_high_ang_z(idx_))
        hand_high_ang_z(idx_) = hand_ang(idx_, 3);
    end
    if(hand_ang(idx_, 3)<hand_low_ang_z(idx_))
        hand_low_ang_z(idx_) = hand_ang(idx_, 3);
    end
    
    if(sd(1,i)==max_)
        
        upper_coord(1,:) = [];
        lower_coord(1,:) = [];
        hand_coord(1,:) = [];
        
        upper_ang(1,:) = [];
        lower_ang(1,:) = [];
        hand_ang(1,:) = [];
        
        upper_coord_set_x{idx} = upper_coord(:,1);
        upper_coord_set_y{idx} = upper_coord(:,2);
        upper_coord_set_z{idx} = upper_coord(:,3);
        upper_ang_set_x{idx} = upper_ang(:,1);
        upper_ang_set_y{idx} = upper_ang(:,2);
        upper_ang_set_z{idx} = upper_ang(:,3);
        
        lower_coord_set_x{idx} = lower_coord(:,1);
        lower_coord_set_y{idx} = lower_coord(:,2);
        lower_coord_set_z{idx} = lower_coord(:,3);
        lower_ang_set_x{idx} = lower_ang(:,1);
        lower_ang_set_y{idx} = lower_ang(:,2);
        lower_ang_set_z{idx} = lower_ang(:,3);
        
        hand_coord_set_x{idx} = hand_coord(:,1);
        hand_coord_set_y{idx} = hand_coord(:,2);
        hand_coord_set_z{idx} = hand_coord(:,3);
        hand_ang_set_x{idx} = hand_ang(:,1);
        hand_ang_set_y{idx} = hand_ang(:,2);
        hand_ang_set_z{idx} = hand_ang(:,3);
        
        upper_coord_set{idx} = upper_coord;
        lower_coord_set{idx} = lower_coord;
        hand_coord_set{idx} = hand_coord;
        upper_ang_set{idx} = upper_ang;
        lower_ang_set{idx} = lower_ang;
        hand_ang_set{idx} = hand_ang;
        
        upper_coord =[0, 0, 0];
        lower_coord =[0, 0, 0];
        hand_coord =[0, 0, 0];

        upper_ang =[0, 0, 0];
        lower_ang =[0, 0, 0];
        hand_ang =[0, 0, 0];
        
        idx = idx + 1;
    end
end

upper_coord_set
for (i=1:numDemos)
    upper_coord_set_x{i} = upper_coord_set{i}(:,1);
    upper_coord_set_y{i} = upper_coord_set{i}(:,2);
    upper_coord_set_z{i} = upper_coord_set{i}(:,3);
    
    temp = upper_coord_set{1, i};
    for(j=1:demoSize);
        r=0.3;
        x = temp(j, 1);
        y = temp(j, 2);
        z = temp(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [2*r*sin(ay)*sin(az), 2*r*sin(ay)*cos(az),  2*r*cos(ay)];

        temp(j,1) = xzy(1);
        temp(j,3) = xzy(2);
        temp(j,2) = xzy(3);

        if(temp(j,1)>upper_high_x_2(i))
           upper_high_x_2(i) = temp(j,1);
        end
        if(temp(j,1)<upper_low_x_2(i))
           upper_low_x_2(i) = temp(j,1);
        end
        if(temp(j,3)>upper_high_z_2(i))
           upper_high_z_2(i) = temp(j,3);
        end
        if(temp(j,3)<upper_low_z_2(i))
            upper_high_y_2(i) = temp(j,2);
        end
        if(temp(j,2)<upper_low_y_2(i))
            upper_low_y_2(i) = temp(j,2);
        end
        if(temp(j,2)>upper_high_y_2(i))
            upper_high_y_2(i) = temp(j,2);
        end
    end
    upper_coord_set_2{i} = temp;
    
    upper_coord_set_x_2{i} = upper_coord_set_2{i}(:,1);
    upper_coord_set_y_2{i} = upper_coord_set_2{i}(:,2);
    upper_coord_set_z_2{i} = upper_coord_set_2{i}(:,3);
    
    prev = upper_coord_set_2{i};
    temp = lower_coord_set{i};
    r=0.3;
    for(j=1:demoSize)
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [2*r*sin(ay)*sin(az), 2*r*sin(ay)*cos(az),  2*r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>lower_high_x(j))
            lower_high_x(j) = temp(j,1);
        end
        if(temp(j,1)<lower_low_x(j))
            lower_low_x(j) = temp(j,1);
        end
        if(temp(j,3)>lower_high_z(j))
            lower_high_z(j) = temp(j,3);
        end
        if(temp(j,3)<lower_low_z(j))
            lower_low_z(j) = temp(j,3);
        end
        if(temp(j,2)>lower_high_y(j))
            lower_high_y(j) = temp(j,2);
        end
        if(temp(j,2)<lower_low_y(j))
            lower_low_y(j) = temp(j,2);
        end
    end
    lower_coord_set{i} = temp;
    
    lower_coord_set_x{i} = lower_coord_set{i}(:,1);
    lower_coord_set_y{i} = lower_coord_set{i}(:,2);
    lower_coord_set_z{i} = lower_coord_set{i}(:,3);
    
    prev = lower_coord_set{i};
    temp = lower_coord_set{i};
    r=0.3;
    for(j=1:size(temp,1))
        
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        if(temp(j,1)>lower_high_x_2(j))
            lower_high_x_2(j) = temp(j,1);
        end
        if(temp(j,1)<lower_low_x_2(j))
            lower_low_x_2(j) = temp(j,1);
        end
        if(temp(j,3)>lower_high_z_2(j))
            lower_high_z_2(j) = temp(j,3);
        end
        if(temp(j,3)<lower_low_z_2(j))
            lower_low_z_2(j) = temp(j,3);
        end
        if(temp(j,2)>lower_high_y_2(j))
            lower_high_y_2(j) = temp(j,2);
        end
        if(temp(j,2)<lower_low_y_2(j))
            lower_low_y_2(j) = temp(j,2);
        end
    end
    lower_coord_set_2{i} = temp;
    
    lower_coord_set_x_2{i} = lower_coord_set_2{i}(:,1);
    lower_coord_set_y_2{i} = lower_coord_set_2{i}(:,2);
    lower_coord_set_z_2{i} = lower_coord_set_2{i}(:,3);
    
    prev = lower_coord_set_2{i};
    temp = lower_coord_set_2{i};
    r=0.05;
    for(j=1:size(temp,1))
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>hand_high_x(j))
            hand_high_x(j) = temp(j,1);
        end
        if(temp(j,1)<hand_low_x(j))
            hand_low_x(j) = temp(j,1);
        end
        if(temp(j,3)>hand_high_z(j))
            hand_high_z(j) = temp(j,3);
        end
        if(temp(j,3)<hand_low_z(j))
            hand_low_z(j) = temp(j,3);
        end
        if(temp(j,2)>hand_high_y(j))
            hand_high_y(j) = temp(j,2);
        end
        if(temp(j,2)<hand_low_y(j))
            hand_low_y(j) = temp(j,2);
        end
    end
    hand_coord_set{i} = temp;
    
    hand_coord_set_x{i} = hand_coord_set{i}(:,1);
    hand_coord_set_y{i} = hand_coord_set{i}(:,2);
    hand_coord_set_z{i} = hand_coord_set{i}(:,3);
    
    prev = hand_coord_set{i};
    temp = hand_coord_set{i};
    r=0.05;
    for(j=1:size(temp,1))
        x = temp(j, 1) + prev(j, 1);
        y = temp(j, 2) + prev(j, 2);
        z = temp(j, 3) + prev(j, 3);
        ax = atan2(sqrt(y^2+z^2),x);
        ay = atan2(sqrt(z^2+x^2),y);
        az = atan2(sqrt(x^2+y^2),z);
        xzy = [r*sin(ay)*sin(az), r*sin(ay)*cos(az),  r*cos(ay)];
        
        temp(j,1) = temp(j, 1) + xzy(1);
        temp(j,3) = temp(j, 3) + xzy(2);
        temp(j,2) = temp(j, 2) + xzy(3);
        
        if(temp(j,1)>hand_high_x_2(j))
            hand_high_x_2(j) = temp(j,1);
        end
        if(temp(j,1)<hand_low_x_2(j))
            hand_low_x_2(j) = temp(j,1);
        end
        if(temp(j,3)>hand_high_z_2(j))
            hand_high_z_2(j) = temp(j,3);
        end
        if(temp(j,3)<hand_low_z_2(j))
            hand_low_z_2(j) = temp(j,3);
        end
        if(temp(j,2)>hand_high_y_2(j))
            hand_high_y_2(j) = temp(j,2);
        end
        if(temp(j,2)<hand_low_y_2(j))
            hand_low_y_2(j) = temp(j,2);
        end
    end
    hand_coord_set_2{i} = temp;
    
    hand_coord_set_x_2{i} = hand_coord_set_2{i}(:,1);
    hand_coord_set_y_2{i} = hand_coord_set_2{i}(:,2);
    hand_coord_set_z_2{i} = hand_coord_set_2{i}(:,3);
end



upper_coord_set_2
upperset{1} =  upper_coord_set{1} ;
upperset{2} = upper_coord_set_2{1};
upperset{3} = upper_coord_set_x{1};
upperset{4} = upper_coord_set_x_2{1};
upperset{5} = upper_coord_set_y{1};
upperset{6} = upper_coord_set_y_2{1};
upperset{7} = upper_coord_set_z{1};
upperset{8} = upper_coord_set_z_2{1};
upperset{9} = upper_low_x;
upperset{10} = upper_low_x_2;
upperset{11} = upper_low_y;
upperset{12} = upper_low_y_2;
upperset{13} = upper_low_z;
upperset{14} = upper_low_z_2;
upperset{15} = upper_high_x;
upperset{16} = upper_high_x_2;
upperset{17} = upper_high_y;
upperset{18} = upper_high_y_2;
upperset{19} = upper_high_z;
upperset{20} = upper_high_z_2;
upperset{21} = upper_ang;
upperset{23} = upper_high_ang_x;
upperset{24} = upper_high_ang_y;
upperset{25} = upper_high_ang_z;
upperset{26} = upper_low_ang_x;
upperset{27} = upper_low_ang_y;
upperset{28} = upper_low_ang_z;

lowerset={}
lowerset{1} =  lower_coord_set{1} ;
lowerset{2} = lower_coord_set_2{1};
lowerset{3} = lower_coord_set_x{1};
lowerset{4} = lower_coord_set_x_2{1};
lowerset{5} = lower_coord_set_y{1};
lowerset{6} = lower_coord_set_y_2{1};
lowerset{7} = lower_coord_set_z{1};
lowerset{8} = lower_coord_set_z_2{1};
lowerset{9} = lower_low_x;
lowerset{10} = lower_low_x_2;
lowerset{11} = lower_low_y;
lowerset{12} = lower_low_y_2;
lowerset{13} = lower_low_z;
lowerset{14} = lower_low_z_2;
lowerset{15} = lower_high_x;
lowerset{16} = lower_high_x_2;
lowerset{17} = lower_high_y;
lowerset{18} = lower_high_y_2;
lowerset{19} = lower_high_z;
lowerset{20} = lower_high_z_2;
lowerset{21} = lower_ang;
lowerset{23} = lower_high_ang_x;
lowerset{24} = lower_high_ang_y;
lowerset{25} = lower_high_ang_z;
lowerset{26} = lower_low_ang_x;
lowerset{27} = lower_low_ang_y;
lowerset{28} = lower_low_ang_z;


handset={}
handset{1} =  hand_coord_set{1} ;
handset{2} = hand_coord_set_2{1};
handset{3} = hand_coord_set_x{1};
handset{4} = hand_coord_set_x_2{1};
handset{5} = hand_coord_set_y{1};
handset{6} = hand_coord_set_y_2{1};
handset{7} = hand_coord_set_z{1};
handset{8} = hand_coord_set_z_2{1};
handset{9} = hand_low_x;
handset{10} = hand_low_x_2;
handset{11} = hand_low_y;
handset{12} = hand_low_y_2;
handset{13} = hand_low_z;
handset{14} = hand_low_z_2;
handset{15} = hand_high_x;
handset{16} = hand_high_x_2;
handset{17} = hand_high_y;
handset{18} = hand_high_y_2;
handset{19} = hand_high_z;
handset{20} = hand_high_z_2;
handset{21} = hand_ang;
handset{23} = hand_high_ang_x;
handset{24} = hand_high_ang_y;
handset{25} = hand_high_ang_z;
handset{26} = hand_low_ang_x;
handset{27} = hand_low_ang_y;
handset{28} = hand_low_ang_z;

for(i = 2:numDemos)
    upperset{1,1} = [upperset{1} ; upper_coord_set{i}];
    upperset{1,2} = [upperset{2} ; upper_coord_set_2{i}];
    upperset{3} = [upperset{3} ; upper_coord_set_x{i}];
    upperset{4} = [upperset{4} ; upper_coord_set_x_2{i}];
    upperset{5} = [upperset{4} ; upper_coord_set_y{i}];
    upperset{6} = [upperset{6} ; upper_coord_set_y_2{i}];
    upperset{7} = [upperset{7} ; upper_coord_set_z{i}];
    upperset{8} = [upperset{8} ; upper_coord_set_z_2{i}];
    
    lowerset{1} = [lowerset{1} ; lower_coord_set{i}];
    lowerset{2} = [lowerset{2} ; lower_coord_set_2{i}];
    lowerset{3} = [lowerset{3} ; lower_coord_set_x{i}];
    lowerset{4} = [lowerset{4} ; lower_coord_set_x_2{i}];
    lowerset{5} = [lowerset{4} ; lower_coord_set_y{i}];
    lowerset{6} = [lowerset{6} ; lower_coord_set_y_2{i}];
    lowerset{7} = [lowerset{7} ; lower_coord_set_z{i}];
    lowerset{8} = [lowerset{8} ; lower_coord_set_z_2{i}];
    
    handset{1} = [handset{1} ; hand_coord_set{i}];
    handset{2} = [handset{2} ; hand_coord_set_2{i}];
    handset{3} = [handset{3} ; hand_coord_set_x{i}];
    handset{4} = [handset{4} ; hand_coord_set_x_2{i}];
    handset{5} = [handset{4} ; hand_coord_set_y{i}];
    handset{6} = [handset{6} ; hand_coord_set_y_2{i}];
    handset{7} = [handset{7} ; hand_coord_set_z{i}];
    handset{8} = [handset{8} ; hand_coord_set_z_2{i}];
end
save(upper_file, 'upperset');
save(lower_file, 'lowerset');
hand_file
save(hand_file, 'handset');

