# Uses LipGAN to generate lip motion

LipGAN: https://github.com/Rudrabha/LipGAN


## Setup
```
sudo apt-get install ffmpeg
git clone https://github.com/Rudrabha/LipGAN.git

cd LipGAN

pip3 install -q youtube-dl
pip3 install -q git+https://www.github.com/keras-team/keras-contrib.git

cd LipGAN/logs && gdown https://drive.google.com/uc?id=1DtXY5Ei_V6QjrLwfe7YDrmbSCDu6iru1
cd LipGAN/logs && wget -q http://dlib.net/files/mmod_human_face_detector.dat.bz2
cd LipGAN/logs && bzip2 -d mmod_human_face_detector.dat.bz2

wget http://images.zeno.org/Kunstwerke/I/big/1300044a.jpg
wget https://keithito.com/LJ-Speech-Dataset/LJ037-0171.wav

cd matlab
matlab -nodesktop
>> create_mat(input_wav_or_mp4_file, path_to_output.mat) # replace with file paths
>> exit
cd ..

python3 batch_inference.py --checkpoint_path logs/lipgan_residual_mel.h5 --face ../1300044a.jpg --fps 30 --audio ../LJ037-0171.wav --results_dir ..
```


