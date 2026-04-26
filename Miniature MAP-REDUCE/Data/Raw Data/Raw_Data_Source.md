# 📂 Raw Dataset – E-commerce Big Data

This folder is intended to store the **raw dataset** used in this project.

Due to GitHub's file size limitations, the dataset is **not included** in this repository.

---

## 📥 Download Dataset

You can download the dataset from Kaggle:

🔗 [E-commerce Big Data Dataset](https://www.kaggle.com/datasets/anaskhaann/big-data-for-ecommerce)

---

## 📌 Instructions

### Step 1: Download the dataset

* Visit the Kaggle link above
* Download the dataset as a `.zip` file

---

### Step 2: Extract the dataset

* Unzip the downloaded file
* Locate the file:

```
Product_Reviews.csv
```

---

### Step 3: Place the file in this folder

Move the extracted file to:

```
Data/Raw Data/Product_Reviews.csv
```

---

### Step 4: Verify structure

Your folder structure should look like:

```
Map_Reduce_Implementation/
│
├── Data/
│   ├── Raw Data/
│   │   ├── Product_Reviews.csv
│       └── Raw_Data_Source.md
|       

```

---

## ⚠️ Important Notes

* Do **not** upload the dataset to GitHub (it exceeds size limits)
* Ensure the file name remains unchanged:

```
Product_Reviews.csv
```

* The project’s MapReduce engine depends on this exact path

---

The engine will automatically read from:

```
Data/Raw Data/Product_Reviews.csv
```

---

## 💡 Tip

If you face issues:

* Check file path
* Ensure correct file name
* Confirm dataset is properly extracted

---

This setup keeps the repository lightweight while enabling full functionality of the MapReduce engine.
