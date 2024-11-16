# Face Verification Report Generator

This project generates a verification report for face matching. It compares images in a "verification" directory against a "valid" directory, checks for matching admission numbers, counts images, and identifies discrepancies.

## Features
Generates a CSV report with remarks on:
  - Admission number existence.
  - Total number of images.
  - Number of verified images.
  - Discrepancies like empty folders, invalid counts, or mixed datasets.

## Requirements
- Python 3.8 or higher
- Libraries: `os`, `csv`, `numpy`, `scikit-learn`, `dotenv` , `insightface`, `pillow`

## 1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/face-verification-report.git
   cd face-verification-report
 ```  
## 2. Setup the Application

### 1. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies.

#### Linux/Mac:
1. **Create the virtual environment**:
    ```bash
    python3 -m venv venv
    ```
2. **Activate the environment**:
    ```bash
    source venv/bin/activate
    ```

#### Windows:
1. **Create the virtual environment**:
    ```bash
    python -m venv venv
    ```
2. **Activate the environment**:
    ```bash
    venv\Scripts\activate
    ```

## 3. Install Dependencies
Install all required Python libraries from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## 4. Prepare the Directories
Set up the required directory structure in the project folder:

**Valid Directory:**
- Contains reference images, one for each admission number.
- Each image must be named after the admission number (e.g., 12345.jpg).

**Verification Directory:**

- Contains subfolders named after admission numbers.
- Each subfolder must have either 5 or 10 images of the respective person.

**Example directory structure**

```bash
project-folder/
├── valid/
│   ├── 12345.jpg
│   ├── 67890.jpg
│   └── 11223.jpg
├── verification/
│   ├── 12345/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   ├── img3.jpg
│   │   ├── img4.jpg
│   │   └── img5.jpg
│   ├── 67890/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   ├── img3.jpg
│   │   ├── img4.jpg
│   │   └── img5.jpg
│   └── 11223/
│       ├── img1.jpg
│       ├── img2.jpg
│       ├── img3.jpg
│       ├── img4.jpg
│       ├── img5.jpg
│       ├── img6.jpg
│       ├── img7.jpg
│       ├── img8.jpg
│       ├── img9.jpg
│       └── img10.jpg
```
## 5. Run the Application
Execute the script to generate the report:

```bash
python main.py
```
### Example Output
The script generates a CSV file (default: verification_report.csv) with the following information:
<table>
  <thead>
    <tr>
      <th>Folder Name</th>
      <th>Admission Number Exists?</th>
      <th>No. of Images</th>
      <th>No. of Verified Images</th>
      <th>Data Count Remark</th>
      <th>Directory Remark</th>
      <th>Verification Status Remark</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>12345</td>
      <td>Yes</td>
      <td>5</td>
      <td>5</td>
      <td>✔</td>
      <td>✔</td>
      <td>✔</td>
    </tr>
    <tr>
      <td>67890</td>
      <td>No</td>
      <td>6</td>
      <td>0</td>
      <td>Invalid Data Count</td>
      <td>Verification data does not exist</td>
      <td>No Dataset</td>
    </tr>
    <tr>
      <td>11223</td>
      <td>Yes</td>
      <td>10</td>
      <td>8</td>
      <td>✔</td>
      <td>✔</td>
      <td>Mixed Dataset</td>
    </tr>
  </tbody>
</table>


