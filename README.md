<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="data/logo.png" alt="logo" width="50" height="50">

<h3 align="center">Face Recognition Sys</h3>
<a href="./README_ch.md">Chinese</a>

</div>
 

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
<div align="center">
<img src="data/image-5.png" alt="demo1" width="400" height="250">
</div>
This system implements face recognition based on YOLOV5s + ArcFace/FaceNet. The YOLOV5s model is used for face detection, ArcFace/FaceNet is used for face recognition, and PySide2 + Qt Designer is used to design the system UI.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Getting Started

This is an example of how you may set up your project locally.
To get a local copy up and running follow these simple example steps.


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/qqizhao/FaceRecognitionSys
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

1. Start the system
```sh
python login.py

python window.py  # If you do not need to upload the recognition results to the database, you can directly run window.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b your-branch-name`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin your-branch-name`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* https://blog.csdn.net/qq_41334243/article/details/107425492  
* https://blog.csdn.net/weixin_41809530/article/details/107313752  
* https://github.com/BlackFeatherQQ/FaceRecognition?login=from_csdn  
* https://github.com/ultralytics/yolov5 


<p align="right">(<a href="#readme-top">back to top</a>)</p>