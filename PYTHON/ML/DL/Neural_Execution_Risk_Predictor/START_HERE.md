# 🚀 EXECUTION GUIDE - Start Here!

## Welcome to Neural Execution Risk Predictor!

This guide will get you up and running in **5 simple steps**.

---

## ⚡ Quick Start (5 Steps)

### Step 1: Open Jupyter Notebook

```bash
cd "D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor"
jupyter notebook
```

### Step 2: Open the Main Notebook

In Jupyter, open:
```
neural_execution_risk_predictor.ipynb
```

### Step 3: Install Dependencies (First Cell)

The first code cell will check dependencies. If needed, run:
```bash
pip install -r requirements.txt
```

### Step 4: Run All Cells

In Jupyter: **Cell → Run All**

This will:
- ✅ Extract features from BPI Challenge 2012 (if XES file exists)
- ✅ Generate synthetic execution plans
- ✅ Combine datasets
- ✅ Train neural network
- ✅ Evaluate model
- ✅ Generate visualizations
- ✅ Save model artifacts

**Estimated Time:** 10-15 minutes (CPU) | 5-7 minutes (GPU)

### Step 5: Check Outputs

After completion, you'll have:

**Model Files:**
- `model/risk_model.h5` (trained model)
- `model/scaler.joblib` (feature scaler)
- `model/model_metadata.json` (model info)

**Visualizations:**
- `reports/training_curves.png`
- `reports/confusion_matrix.png`
- `reports/feature_importance.png`

**Data:**
- `data/execution_risk_dataset.csv` (combined dataset)

---

## 🎯 Alternative: Quick Start Notebook

For a streamlined experience:

```bash
jupyter notebook quick_start.ipynb
```

This notebook:
- Auto-installs dependencies
- Guides you step-by-step
- Has helpful error messages
- Takes ~10 minutes

---

## 🌐 Optional: Start the API

After training, test the REST API:

**Terminal 1: Start API**
```bash
cd "D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor"
uvicorn api.main:app --reload
```

**Terminal 2: Test API**
```bash
python test_api.py
```

**Or visit in browser:**
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 🐳 Optional: Docker Deployment

Build and run in container:

```bash
# Build
docker build -t neural-risk-predictor .

# Run
docker run -p 8000:8000 neural-risk-predictor

# Test
curl http://localhost:8000/health
```

---

## ❓ What if XES File is Missing?

**Don't worry!** The system will work fine with synthetic data only.

If you see:
```
⚠ XES file not found: new_BPI_Challenge_2012.xes
```

Just continue - the notebook will:
- Skip BPI extraction
- Generate ~2,000 synthetic samples
- Train successfully

**To add BPI data later:**
1. Place `new_BPI_Challenge_2012.xes` in project root
2. Re-run notebook

---

## 🔧 Troubleshooting

### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
```bash
# Use different port
uvicorn api.main:app --port 8001
```

### Issue: TensorFlow warnings about GPU
**Ignore it!** CPU is fine for this project.

### Issue: Notebook kernel crashes
**Restart kernel:**
- Jupyter: Kernel → Restart & Run All

---

## 📊 What to Expect

### Training Output (Example)

```
Epoch 1/30
450/450 [==============================] - 2s 4ms/step
loss: 0.7234 - accuracy: 0.6821 - val_loss: 0.4567 - val_accuracy: 0.8234
...
Epoch 18/30
450/450 [==============================] - 2s 3ms/step
loss: 0.1523 - accuracy: 0.9412 - val_loss: 0.1876 - val_accuracy: 0.9387

Early stopping triggered!
✓ Model training complete!
```

### Evaluation Output (Example)

```
Test Accuracy: 0.9431
Test Loss: 0.1872

Per-Class Metrics:
  LOW_RISK    - Precision: 0.9612, Recall: 0.9701
  MEDIUM_RISK - Precision: 0.9123, Recall: 0.8934
  HIGH_RISK   - Precision: 0.9534, Recall: 0.9612
```

### Visualizations Generated

1. **Training Curves** - Loss and accuracy over epochs
2. **Confusion Matrix** - Model predictions vs actual
3. **Feature Importance** - Which features matter most
4. **Feature Distributions** - Data exploration plots

---

## 📚 Documentation Links

- **README.md** - Complete technical documentation
- **PROJECT_SUMMARY.md** - Quick reference guide
- **CHECKLIST.md** - Implementation verification
- **API Docs** - http://localhost:8000/docs (when API running)

---

## 🎓 Learning Path

**Beginner?** Follow this order:

1. Run `quick_start.ipynb` (simple, guided)
2. Explore `neural_execution_risk_predictor.ipynb` (full details)
3. Read `README.md` (understand architecture)
4. Test API with `test_api.py` (see it in action)
5. Review code in `model/train.py` (learn implementation)

**Advanced?** Jump straight to:

1. `neural_execution_risk_predictor.ipynb` (full pipeline)
2. Modify architecture in code cells
3. Experiment with hyperparameters
4. Deploy to cloud

---

## 🔬 Experimentation Ideas

Want to try something new?

1. **Adjust Model Architecture**
   - Add more layers: Dense(128) → Dense(64) → Dense(32)
   - Change dropout: try 0.3 or 0.4
   - Different activation: try LeakyReLU

2. **Tune Hyperparameters**
   - Learning rate: try 0.0001 or 0.01
   - Batch size: try 16 or 64
   - Epochs: increase to 50

3. **Feature Engineering**
   - Add new features (edit scripts)
   - Remove features (drop columns)
   - Feature interactions (multiply features)

4. **Risk Thresholds**
   - Change labeling rules in `generate_synthetic_plans.py`
   - Make HIGH_RISK more/less strict

---

## ✅ Success Checklist

After running, verify:

- [ ] `model/risk_model.h5` exists (~5 MB)
- [ ] `reports/` has 4-5 PNG images
- [ ] Test accuracy > 90%
- [ ] API starts without errors
- [ ] Sample predictions make sense

If all checked → **Success!** 🎉

---

## 🆘 Need Help?

1. **Check logs** in notebook cells
2. **Read error messages** carefully
3. **Review README.md** for details
4. **Check CHECKLIST.md** for verification
5. **Inspect code** in failing script

---

## 🎯 Your Next Action

**👉 Open Jupyter and run `neural_execution_risk_predictor.ipynb`**

That's it! Everything else is automatic.

---

## 📞 Quick Reference

**Project Path:**
```
D:\JAVA\CODE\PYTHON\ML\DL\Neural Execution Risk Predictor
```

**Main Notebook:**
```
neural_execution_risk_predictor.ipynb
```

**Start API:**
```
uvicorn api.main:app --reload
```

**Test API:**
```
python test_api.py
```

---

**Ready? Let's build safer agent systems!** 🚀

**Status:** ✅ All systems operational and ready to run!
