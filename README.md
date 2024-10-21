# RAG API Documentation

## API Deployment

The API is deployed and accessible at:

[https://rag-hw.onrender.com](https://rag-hw.onrender.com)

## Authentication

All endpoints require authentication using a Bearer token. Include the following header in your requests:

```
Authorization: Bearer token
```

## Endpoints

### 1. Ingest Documents

- **URL**: `https://rag-hw.onrender.com/ingest`
- **Method**: POST
- **Body**:
  ```json
  {
    "files": ["https://example.com/file1.pdf", "https://example.com/file2.txt"],
    "datasetId": "unique_dataset_id"
  }
  ```

### 2. Retrieve Information

- **URL**: `https://rag-hw.onrender.com/retrieve`
- **Method**: POST
- **Body**:
  ```json
  {
    "prompt": "Your query here",
    "datasetId": "unique_dataset_id"
  }
  ```

### 3. Delete Dataset

- **URL**: `https://rag-hw.onrender.com/delete`
- **Method**: DELETE
- **Body**:
  ```json
  {
    "datasetId": "unique_dataset_id"
  }
  ```

## Database Population

The database has been populated with test data. You can use the provided `datasetId` in your requests to interact with this data.

## Example Requests

Here are cURL commands to test the API:

1. Ingest Documents:

```bash
curl -X POST https://rag-hw.onrender.com/ingest \
-H "Authorization: Bearer token" \
-H "Content-Type: application/json" \
-d '{"files": ["https://example.com/file1.pdf"], "datasetId": "test_dataset"}'
```

2. Retrieve Information:

```bash
curl -X POST https://rag-hw.onrender.com/retrieve \
-H "Authorization: Bearer token" \
-H "Content-Type: application/json" \
-d '{"prompt": "What is RAG?", "datasetId": "test_dataset"}'
```

3. Delete Dataset:

```bash
curl -X DELETE https://rag-hw.onrender.com/delete \
-H "Authorization: Bearer token" \
-H "Content-Type: application/json" \
-d '{"datasetId": "test_dataset"}'
```


## GitHub Repository

The source code for this API is available at: [https://github.com/your-username/your-repo](https://github.com/your-username/your-repo)


## Prepopulated Datasets

The following datasets have been prepopulated in the system for testing and demonstration purposes:

1. Dataset 1: Chevrolet Colorado E-Brochure
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/2022-chevrolet-colorado-ebrochure.pdf"
     ],
     "datasetId": "dataset_chevrolet"
   }
   ```

2. Dataset 2: Invoice Example
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/invoice_1.pdf"
     ],
     "datasetId": "dataset_invoice"
   }
   ```

3. Dataset 3: Meditations
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/meidtations.pdf"
     ],
     "datasetId": "dataset_meditations"
   }
   ```

4. Dataset 4: Oppenheimer Applied Cognitive Psychology
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/Oppenheimer-2006-Applied_Cognitive_Psychology.pdf"
     ],
     "datasetId": "dataset_oppenheimer"
   }
   ```

5. Dataset 5: Pretotype It (10 Year Anniversary Edition)
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/pretotype_it_10_year_anniversary_edition__with_cover__1.1.pdf"
     ],
     "datasetId": "dataset_pretotype"
   }
   ```

6. Dataset 6: WEF Global Cooperation Barometer 2024
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/WEF_The_Global_Cooperation_Barometer_2024.pdf"
     ],
     "datasetId": "dataset_wef"
   }
   ```

7. Dataset 7: FlyRNAi Data Baseline
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/FlyRNAi_data_baseline.txt"
     ],
     "datasetId": "dataset_flyrnai"
   }
   ```

8. Dataset 8: Society Studies
   ```json
   {
     "files": [
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/alpha_society.pdf",
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/beta_society.pdf",
       "https://example-files-rag.s3.eu-central-1.amazonaws.com/gamma_society.pdf"
     ],
     "datasetId": "dataset_society"
   }
   ```


You can use these `datasetId` values in your API requests to interact with the prepopulated data.

