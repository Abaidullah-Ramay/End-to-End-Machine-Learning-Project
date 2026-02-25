import os
import pandas as pd
from mlProject import logger
from mlProject.entity.config_entity import DataValidationConfig

class DataValiadtion:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = True
            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)
            all_schema = self.config.all_schema.keys()
            
            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    break # Stop checking if we find a mismatch

            # Write the final status only once
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            if validation_status:
                logger.info("All columns validated successfully against the schema.")
            else:
                logger.warning("Data validation failed. Schema mismatch detected.")

            return validation_status
        
        except Exception as e:
            logger.exception(e)
            raise e