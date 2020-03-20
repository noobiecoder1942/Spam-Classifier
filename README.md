# Spam-Classifier

A spam email classifier from scratch using a Bag-of-Words and a Naive-Bayes model.

Directory Structure is as follows:
```bash
.
+-- spam.py
+-- train
|   +-- spam
|   +-- notspam
+-- test
```
Usage:
```
python3 path_to_train_directory path_to_test_directory output_file_name
```

Output Format:
```
file1_name class
file2_name class
```
where class is either spam or notspam.
