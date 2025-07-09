import pickle
import os
import sys
import inspect
import pandas as pd
import numpy as np

# Try to import common ML libraries to check for their types later
# If you encounter ImportError, uncomment and run:
# pip install scikit-learn numpy pandas

try:
    import sklearn
    from sklearn.base import BaseEstimator
    from sklearn.pipeline import Pipeline
    print(f"Scikit-learn version: {sklearn.__version__}")
except ImportError:
    sklearn = None
    print("Scikit-learn not found. Scikit-learn specific analysis will be skipped.")


def inspect_pkl_file(pkl_file_path):
    """
    Loads a .pkl file and provides basic information about the contained object.
    """
    if not os.path.exists(pkl_file_path):
        print(f"Error: File not found at '{pkl_file_path}'")
        return None

    print(f"\n--- Inspecting '{pkl_file_path}' ---")
    try:
        with open(pkl_file_path, 'rb') as f:
            obj = pickle.load(f)

        print(f"Successfully loaded object from '{pkl_file_path}'.")
        print(f"Object type: {type(obj)}")
        print(f"Object module: {type(obj).__module__}")
        print(f"Object class name: {type(obj).__name__}")

        # Attempt to provide more specific info based on common ML libraries
        if sklearn and isinstance(obj, BaseEstimator):
            print("\nThis appears to be a scikit-learn estimator.")
            analyze_sklearn_model(obj)
        else:
            print("\nThis is a generic Python object. Inferring 'features' is highly dependent on its internal structure.")
            print("Consider inspecting its attributes or documentation for more details.")
            print("Some common attributes:")
            for attr in ['_feature_names', 'columns', 'feature_names', 'input_shape']:
                if hasattr(obj, attr):
                    print(f"  .{attr}: {getattr(obj, attr)}")
            # For custom objects, you might want to print more specific attributes
            # print(f"Object attributes: {dir(obj)}") # Use with caution, can be very verbose

        return obj

    except pickle.UnpicklingError as e:
        print(f"Error: Could not unpickle the file. It might be corrupted or created with a different Python version/library.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while loading or inspecting the file: {e}")
    return None

def analyze_sklearn_model(model):
    """
    Analyzes a scikit-learn model for input feature information.
    """
    print("\n--- Scikit-learn Model Details ---")

    # Check for number of features learned during fit
    if hasattr(model, 'n_features_in_'):
        print(f"  Number of input features (n_features_in_): {model.n_features_in_}")
    else:
        print("  'n_features_in_' attribute not found (common in older scikit-learn versions or specific estimators).")

    # Check for feature names (available in sklearn >= 0.24)
    if hasattr(model, 'feature_names_in_') and model.feature_names_in_ is not None:
        print(f"  Input feature names (feature_names_in_): {list(model.feature_names_in_)}")
    else:
        print("  'feature_names_in_' attribute not found or is None.")
        print("  This attribute is available in scikit-learn versions >= 0.24 and depends on the estimator type.")

    # If it's a Pipeline, try to inspect its components
    if isinstance(model, Pipeline):
        print("\n  This is a scikit-learn Pipeline. Inspecting steps:")
        for step_name, step_estimator in model.steps:
            print(f"    Step: '{step_name}' ({type(step_estimator).__name__})")
            if hasattr(step_estimator, 'n_features_in_'):
                print(f"      n_features_in_ for this step: {step_estimator.n_features_in_}")
            if hasattr(step_estimator, 'feature_names_in_') and step_estimator.feature_names_in_ is not None:
                print(f"      feature_names_in_ for this step: {list(step_estimator.feature_names_in_)}")
            if hasattr(step_estimator, 'get_feature_names_out'):
                try:
                    # For transformers like ColumnTransformer, this can give output feature names
                    # Requires an input to infer, so we'll just note its existence.
                    print("      This step has 'get_feature_names_out()' method (useful for transformers).")
                except Exception:
                    pass # get_feature_names_out often requires an input

    print("\n  Recommendation for Scikit-learn:")
    print("  The best way to know required columns is to refer to the training data used.")
    print("  The `n_features_in_` attribute tells you the number of features.")
    print("  `feature_names_in_` provides names if they were explicitly set or inferred by the model (sklearn >= 0.24).")
    print("  For pipelines, examine the `ColumnTransformer` (if used) to understand preprocessing and column usage.")


def main():
    """
    Main function to handle the inspection.
    """
    print("\n--- PKL File Information Script (Scikit-learn Only) ---")
    print("This script attempts to infer information about the contents of a .pkl file,")
    print("especially regarding expected input features/columns for scikit-learn models.")
    print("Note: .pkl files are generic. Explicit feature names are often not stored directly,")
    print("but we can infer the *number* of features.")

    # --- DEFINE YOUR .PKL FILE PATH HERE ---
    # Replace 'path/to/your_sklearn_model.pkl' with the actual path to your .pkl file.
    # Example: sklearn_pkl_file = 'my_model_folder/my_classifier.pkl'
    sklearn_pkl_file = 'C:\\Users\\Administrator\\Desktop\\Python\\ML\\ProjectPlan\\saved_kmeans_models\\kmeans_Fragile_Only.pkl' # <--- EDIT THIS LINE

    if not os.path.exists(sklearn_pkl_file):
        print(f"\nError: The specified .pkl file does not exist at '{sklearn_pkl_file}'.")
        print("Please edit the 'sklearn_pkl_file' variable in the script to the correct path.")
    else:
        # --- Run Inspection for Scikit-learn Model ---
        print("\n" + "="*50)
        inspect_pkl_file(sklearn_pkl_file)
        print("="*50)

    print("\nScript execution complete.")


if __name__ == "__main__":
    main()