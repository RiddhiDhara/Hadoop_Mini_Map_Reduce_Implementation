# 🚀 Mini MapReduce Engine

## 📌 Overview
This is a guide to show where the processed_data.csv file is stored after the raw dataset Product_Review.csv file is being processed

---

## 🏗️ Processed_data.csv file structure

```
Mini MapReduce/
│
├── Data/
│   ├── Raw Data/
|   |   ├── Product_Reviews.csv
│   ├── Processed Data/
│       ├── processed_data.csv
├── Data Processing Stage/
    ├── processor.ipynb
    
```
---

## ⚙️ Process Flow

1. Load downloaded csv from Kaggle inside [Raw Data] folder
2. Then raw csv is being processed by `processor.ipynb`
3. Export processed dataset as CSV stored inside [Processed Data] folder

---

## 💾 Output Location
/Data/Processed Data/

---

## 🎯 Goal
To make user understand how the CSV file is being stored after processing is done