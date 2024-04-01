<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab.rlp.net/top/24s/profplaner/profplaner_backend">
    <img src="https://gitlab.rlp.net/uploads/-/system/group/avatar/66550/Entwurf_28.png?width=48" alt="ProfPlaner - Logo" width="80" height="80">
  </a>
  <h3 align="center">ProfPlaner - Backend</h3>
  <br />
</div>





<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#technologies">Technologies</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>





<!-- INSTALLATION -->
## Installation

1. Clone the repository
   ```sh
   git clone https://gitlab.rlp.net/top/24s/profplaner/profplaner_backend.git
   ```
2. Import Dummy Data (not for windows)
   ```sh
   docker compose run pp_backend sh import_dummy_data.sh
   ```
3. Run Server
   ```sh
   docker compose up
   ```





<!-- Testing -->
## Testing

1. Run all tests
   ```sh
   docker compose run pp_backend pytest
   ```


## Disclaimer

To be able to make full use of the Site, you'll also need the code from https://github.com/Lormdo/ProfPlanerFront


<!-- TECHNOLOGIES -->
## Technologies
This Project uses Python3.11 with mongodb and FastAPI. The following pip packages were used:
- fastapi
- uvicorn
- pydantic
- pymongo
- pytest
- httpx
- pandas
- XlsxWriter
- python-multipart
- openpyxl



<!-- LICENSE -->
## License

Distributed under the Server Side Public License, v 1. See `LICENSE` for more information.
