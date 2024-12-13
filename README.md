# README

## Main Issues and Challenges Found

- **Hierarchical Relationships**: Handling the hierarchical structure of `Channels` and `Subchannels` required careful design to ensure proper database relations and performance.
- **Dynamic Rating Calculation**: Ratings for `Channels` cannot be stored directly, so a mechanism to compute ratings dynamically was implemented with error handling and logs.
- **Dockerization**: Ensuring the project is containerized for development and testing while maintaining compatibility with PostgreSQL.
- **Efficient Data Export**: Creating a scalable solution to export ratings in a CSV format, including sorting and handling undefined values gracefully.
- **API Design**: Designing flexible endpoints that support hierarchical queries and filtering by groups.

---

## Models Overview (`models.py`)

- **`Group` Model**:
  - Represents a logical grouping of `Channels`.
  - Supports many-to-many relationships with `Channels`.

- **`Content` Model**:
  - Represents individual pieces of media (e.g., videos, PDFs, text).
  - Includes a `metadata` field for arbitrary details and a `rating` field for content evaluation.

- **`Channel` Model**:
  - Hierarchical structure for organizing `Content` and `Subchannels`.
  - Supports dynamic rating calculation based on contents or subchannels.
  - Groups can be associated with channels, with inherited group membership for subchannels.

---

## Endpoints Overview (`urls.py`)

- **`/api/channels/`** (GET, POST, PUT, DELETE):
  - Retrieve, create, update, or delete channels.
  - Supports filtering by `group` using query parameters.

- **`/api/contents/`** (GET, POST, PUT, DELETE):
  - Retrieve, create, update, or delete content.

- **`/api/groups/`** (GET, POST, PUT, DELETE):
  - Retrieve, create, update, or delete groups.

---

## Management Commands

### Export Ratings to CSV

- Command: `export_ratings`
- Usage:
  ```bash
  python manage.py export_ratings
  ```
- Functionality:
  - Exports the ratings of all channels into a CSV file (`channel_ratings.csv`).
  - Includes the `Channel Title` and `Average Rating`.
  - Handles errors gracefully with logs.

### Populate Database with Sample Data

- Command: `populate_data`
- Usage:
  ```bash
  python manage.py populate_data
  ```
- Functionality:
  - Adds sample `Groups`, `Contents`, and `Channels` to the database for testing.
  - Demonstrates relationships and dynamic rating calculation.

---

## Starting the Docker Environment for Testing

1. **Build the Docker Containers**:
   ```bash
   docker-compose build
   ```

2. **Run the Containers**:
   ```bash
   docker-compose up
   ```

3. **Access the Django Container**:
   ```bash
   docker exec -it django_backend_test bash
   ```

4. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional for Admin Access)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate Sample Data**:
   ```bash
   python manage.py populate_data
   ```

7. **Test Endpoints**:
   - Access the API at `http://127.0.0.1:8000/api/`.
   - Use tools like Postman or `cURL` for testing.

8. **Export Ratings**:
   ```bash
   python manage.py export_ratings
   ```
   Verify the output in the generated `channel_ratings.csv` file.

---