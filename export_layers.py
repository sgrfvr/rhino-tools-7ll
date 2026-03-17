import rhino3dm as rhino
import csv
import os

def export_layers_to_csv(file_path, model_path=None):
    """
    Exports the names and properties of all objects in a Rhino model,
    categorized by their layers, to a CSV file.

    Args:
        file_path (str): The file path where the CSV will be saved.
        model_path (str): Path to the Rhino 3dm file. If None, assumes running in Rhino.
    """
    if not file_path.lower().endswith('.csv'):
        print("Error: The file path must end with .csv extension.")
        return

    # Prepare to write to CSV
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            fieldnames = ['Layer', 'Object Name', 'Object Type', 'Color', 'Material']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()

            # If model_path is provided, read from file
            if model_path:
                model = rhino.File3dm.Read(model_path)
                if not model:
                    print(f"Error: Could not read model from {model_path}")
                    return
                
                # Get all layers
                layers = [layer.Name for layer in model.Layers]
                if not layers:
                    print("Warning: No layers found in the model.")
                    return

                for layer in model.Layers:
                    layer_name = layer.Name
                    
                    # Get objects in the current layer
                    for obj in model.Objects:
                        if obj.Attributes.LayerIndex == layer.Index:
                            # Gather object properties
                            obj_name = obj.Attributes.Name if obj.Attributes.Name else "Unnamed"
                            obj_type = str(obj.Geometry.ObjectType) if hasattr(obj.Geometry.ObjectType, '__str__') else type(obj.Geometry).__name__
                            
                            # Handle color safely
                            if hasattr(obj.Attributes, 'ObjectColor') and obj.Attributes.ObjectColor:
                                obj_color = str(obj.Attributes.ObjectColor)
                            else:
                                obj_color = "No Color"
                            
                            obj_material = str(obj.Attributes.MaterialIndex) if obj.Attributes.MaterialIndex >= 0 else "No Material"

                            # Write object info to CSV
                            writer.writerow({
                                'Layer': layer_name,
                                'Object Name': obj_name,
                                'Object Type': obj_type,
                                'Color': obj_color,
                                'Material': obj_material
                            })
            else:
                print("Error: model_path is required when not running inside Rhino")
                return
                
            print(f"Exported object layers and properties to {file_path}")

    except Exception as e:
        print(f"An error occurred while exporting: {e}")

# Example usage
if __name__ == "__main__":
    # TODO: Add user input for file path or integrate with a UI for better experience
    output_file = "exported_layers.csv"
    model_file = "example.3dm"  # Path to your 3dm file
    export_layers_to_csv(output_file, model_file)
