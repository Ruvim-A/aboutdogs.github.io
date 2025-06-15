from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class DogBreed(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    size: str
    temperament: str
    origin: str
    lifespan: str
    weight: str
    height: str
    care_level: str
    exercise_needs: str
    good_with_kids: bool
    good_with_pets: bool
    grooming_needs: str
    image_url: str
    description: str
    health_issues: List[str]
    breed_group: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DogBreedCreate(BaseModel):
    name: str
    size: str
    temperament: str
    origin: str
    lifespan: str
    weight: str
    height: str
    care_level: str
    exercise_needs: str
    good_with_kids: bool
    good_with_pets: bool
    grooming_needs: str
    image_url: str
    description: str
    health_issues: List[str]
    breed_group: str

# Dog breeds data
DOG_BREEDS_DATA = [
    {
        "name": "Golden Retriever",
        "size": "Large",
        "temperament": "Friendly, Intelligent, Devoted",
        "origin": "Scotland",
        "lifespan": "10-12 years",
        "weight": "55-75 lbs",
        "height": "21-24 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1558788353-f76d92427f16",
        "description": "Golden Retrievers are friendly, intelligent, and devoted dogs. They are great family pets and are known for their patience with children.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Heart Disease"],
        "breed_group": "Sporting"
    },
    {
        "name": "German Shepherd",
        "size": "Large",
        "temperament": "Confident, Courageous, Smart",
        "origin": "Germany",
        "lifespan": "9-13 years",
        "weight": "50-90 lbs",
        "height": "22-26 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1453487977089-77350a275ec5",
        "description": "German Shepherds are extremely versatile, serving as family companions, guard dogs, and service dogs.",
        "health_issues": ["Hip Dysplasia", "Bloat", "Degenerative Myelopathy"],
        "breed_group": "Herding"
    },
    {
        "name": "French Bulldog",
        "size": "Small",
        "temperament": "Adaptable, Playful, Smart",
        "origin": "France",
        "lifespan": "10-12 years",
        "weight": "16-28 lbs",
        "height": "11-13 inches",
        "care_level": "Low",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/160846/french-bulldog-summer-smile-joy-160846.jpeg",
        "description": "French Bulldogs are charming, adaptable companions that make excellent apartment dogs.",
        "health_issues": ["Brachycephalic Syndrome", "Hip Dysplasia", "Allergies"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Labrador Retriever",
        "size": "Large",
        "temperament": "Friendly, Outgoing, Active",
        "origin": "Canada",
        "lifespan": "10-12 years",
        "weight": "55-80 lbs",
        "height": "21-25 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/19757632/pexels-photo-19757632.jpeg",
        "description": "Labs are friendly, outgoing, and active companions who have more than enough affection to go around for a family looking for a medium to large dog.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Eye Problems"],
        "breed_group": "Sporting"
    },
    {
        "name": "Poodle",
        "size": "Medium",
        "temperament": "Active, Alert, Intelligent",
        "origin": "Germany",
        "lifespan": "12-15 years",
        "weight": "45-70 lbs",
        "height": "15+ inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/3299899/pexels-photo-3299899.jpeg",
        "description": "Poodles are exceptional jumpers, so pet parents should ensure their fences are high enough to prevent escapes.",
        "health_issues": ["Hip Dysplasia", "Progressive Retinal Atrophy", "Bloat"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Beagle",
        "size": "Medium",
        "temperament": "Friendly, Curious, Merry",
        "origin": "England",
        "lifespan": "12-15 years",
        "weight": "20-30 lbs",
        "height": "13-15 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/38008/pexels-photo-38008.jpeg",
        "description": "Beagles are loving, lovable, happy, easygoing, and companionable – all qualities that make them excellent family dogs.",
        "health_issues": ["Hip Dysplasia", "Cherry Eye", "Epilepsy"],
        "breed_group": "Hound"
    },
    {
        "name": "Rottweiler",
        "size": "Large",
        "temperament": "Loyal, Loving, Confident Guardian",
        "origin": "Germany",
        "lifespan": "8-10 years",
        "weight": "80-135 lbs",
        "height": "22-27 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/170325/pexels-photo-170325.jpeg",
        "description": "Rottweilers are loyal, loving, confident guardians who are very devoted to their families.",
        "health_issues": ["Hip Dysplasia", "Heart Problems", "Cancer"],
        "breed_group": "Working"
    },
    {
        "name": "Yorkshire Terrier",
        "size": "Small",
        "temperament": "Affectionate, Sprightly, Tomboyish",
        "origin": "England",
        "lifespan": "13-16 years",
        "weight": "4-7 lbs",
        "height": "7-8 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/1420405/pexels-photo-1420405.jpeg",
        "description": "Yorkies are affectionate, sprightly, and tomboyish. They make great watchdogs despite their small size.",
        "health_issues": ["Luxating Patella", "Tracheal Collapse", "Dental Problems"],
        "breed_group": "Toy"
    },
    {
        "name": "Bulldog",
        "size": "Medium",
        "temperament": "Docile, Willful, Friendly",
        "origin": "England",
        "lifespan": "8-10 years",
        "weight": "40-50 lbs",
        "height": "14-15 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/776078/pexels-photo-776078.jpeg",
        "description": "Bulldogs are docile, willful, and friendly dogs that make excellent companions for families.",
        "health_issues": ["Brachycephalic Syndrome", "Hip Dysplasia", "Cherry Eye"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Dachshund",
        "size": "Small",
        "temperament": "Friendly, Curious, Spunky",
        "origin": "Germany",
        "lifespan": "12-15 years",
        "weight": "11-32 lbs",
        "height": "5-9 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/169524/pexels-photo-169524.jpeg",
        "description": "Dachshunds are friendly, curious, and spunky dogs known for their distinctive long bodies and short legs.",
        "health_issues": ["Intervertebral Disc Disease", "Obesity", "Dental Issues"],
        "breed_group": "Hound"
    },
    {
        "name": "Siberian Husky",
        "size": "Large",
        "temperament": "Loyal, Outgoing, Mischievous",
        "origin": "Siberia",
        "lifespan": "12-15 years",
        "weight": "35-60 lbs",
        "height": "20-24 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.pexels.com/photos/3715587/pexels-photo-3715587.jpeg",
        "description": "Siberian Huskies are loyal, outgoing, and mischievous dogs bred for sledding in harsh Arctic conditions.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Hypothyroidism"],
        "breed_group": "Working"
    },
    {
        "name": "Border Collie",
        "size": "Medium",
        "temperament": "Affectionate, Smart, Energetic",
        "origin": "England/Scotland",
        "lifespan": "12-15 years",
        "weight": "30-55 lbs",
        "height": "18-22 inches",
        "care_level": "Very High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1649535444934-c33b4a1eee65",
        "description": "Border Collies are affectionate, smart, and energetic dogs that excel at herding and agility sports.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Epilepsy"],
        "breed_group": "Herding"
    },
    {
        "name": "Australian Shepherd",
        "size": "Medium",
        "temperament": "Smart, Work-Oriented, Exuberant",
        "origin": "United States",
        "lifespan": "12-15 years",
        "weight": "40-65 lbs",
        "height": "18-23 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.pexels.com/photos/32551702/pexels-photo-32551702.jpeg",
        "description": "Australian Shepherds are smart, work-oriented, and exuberant dogs that thrive with active families.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Eye Problems"],
        "breed_group": "Herding"
    },
    {
        "name": "Jack Russell Terrier",
        "size": "Small",
        "temperament": "Alert, Curious, Lively",
        "origin": "England",
        "lifespan": "13-16 years",
        "weight": "9-15 lbs",
        "height": "10-12 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/32556788/pexels-photo-32556788.png",
        "description": "Jack Russell Terriers are alert, curious, and lively dogs with boundless energy and intelligence.",
        "health_issues": ["Luxating Patella", "Eye Problems", "Deafness"],
        "breed_group": "Terrier"
    },
    {
        "name": "Dalmatian",
        "size": "Medium",
        "temperament": "Dignified, Smart, Outgoing",
        "origin": "Croatia",
        "lifespan": "11-13 years",
        "weight": "45-70 lbs",
        "height": "19-24 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/5483455/pexels-photo-5483455.jpeg",
        "description": "Dalmatians are dignified, smart, and outgoing dogs famous for their distinctive spotted coat.",
        "health_issues": ["Deafness", "Kidney Stones", "Skin Allergies"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Samoyed",
        "size": "Large",
        "temperament": "Adaptable, Friendly, Gentle",
        "origin": "Siberia",
        "lifespan": "12-14 years",
        "weight": "35-65 lbs",
        "height": "19-24 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.unsplash.com/photo-1554956615-1ba6dc39921b",
        "description": "Samoyeds are adaptable, friendly, and gentle dogs with a beautiful white coat and perpetual smile.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Diabetes"],
        "breed_group": "Working"
    },
    {
        "name": "Chihuahua",
        "size": "Small",
        "temperament": "Graceful, Charming, Sassy",
        "origin": "Mexico",
        "lifespan": "14-16 years",
        "weight": "2-6 lbs",
        "height": "5-8 inches",
        "care_level": "Moderate",
        "exercise_needs": "Low",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/32567176/pexels-photo-32567176.jpeg",
        "description": "Chihuahuas are graceful, charming, and sassy dogs packed with personality in a tiny package.",
        "health_issues": ["Heart Problems", "Eye Problems", "Luxating Patella"],
        "breed_group": "Toy"
    }
]

# Add more breeds to reach 52+
ADDITIONAL_BREEDS = [
    {
        "name": "Boxer",
        "size": "Large",
        "temperament": "Fun-Loving, Bright, Active",
        "origin": "Germany",
        "lifespan": "10-12 years",
        "weight": "65-80 lbs",
        "height": "21-25 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1650908173711-b038152d4de6",
        "description": "Boxers are fun-loving, bright, and active dogs that make excellent family companions.",
        "health_issues": ["Hip Dysplasia", "Heart Problems", "Cancer"],
        "breed_group": "Working"
    },
    {
        "name": "Great Dane",
        "size": "Giant",
        "temperament": "Friendly, Patient, Dependable",
        "origin": "Germany",
        "lifespan": "8-10 years",
        "weight": "110-175 lbs",
        "height": "28-34 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1649535445315-3d6451512402",
        "description": "Great Danes are friendly, patient, and dependable gentle giants despite their imposing size.",
        "health_issues": ["Hip Dysplasia", "Bloat", "Heart Problems"],
        "breed_group": "Working"
    },
    {
        "name": "Shih Tzu",
        "size": "Small",
        "temperament": "Affectionate, Playful, Outgoing",
        "origin": "China",
        "lifespan": "10-18 years",
        "weight": "9-16 lbs",
        "height": "9-11 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.unsplash.com/photo-1728145545225-d4753fe480eb",
        "description": "Shih Tzus are affectionate, playful, and outgoing dogs bred to be companions.",
        "health_issues": ["Brachycephalic Syndrome", "Hip Dysplasia", "Eye Problems"],
        "breed_group": "Toy"
    },
    {
        "name": "Boston Terrier",
        "size": "Small",
        "temperament": "Friendly, Bright, Amusing",
        "origin": "United States",
        "lifespan": "11-13 years",
        "weight": "12-25 lbs",
        "height": "15-17 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/2607544/pexels-photo-2607544.jpeg",
        "description": "Boston Terriers are friendly, bright, and amusing dogs known as the American Gentleman.",
        "health_issues": ["Brachycephalic Syndrome", "Eye Problems", "Deafness"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Cocker Spaniel",
        "size": "Medium",
        "temperament": "Gentle, Smart, Happy",
        "origin": "Spain",
        "lifespan": "12-15 years",
        "weight": "20-30 lbs",
        "height": "13-16 inches",
        "care_level": "High",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1728145547788-9d92ddc7be17",
        "description": "Cocker Spaniels are gentle, smart, and happy dogs that excel as family companions.",
        "health_issues": ["Eye Problems", "Hip Dysplasia", "Ear Infections"],
        "breed_group": "Sporting"
    },
    {
        "name": "Bernese Mountain Dog",
        "size": "Large",
        "temperament": "Good-Natured, Patient, Strong",
        "origin": "Switzerland",
        "lifespan": "6-8 years",
        "weight": "70-115 lbs",
        "height": "23-28 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1728145545724-65fe88157aa6",
        "description": "Bernese Mountain Dogs are good-natured, patient, and strong working dogs from Switzerland.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Cancer"],
        "breed_group": "Working"
    },
    {
        "name": "Mastiff",
        "size": "Giant",
        "temperament": "Courageous, Dignified, Good-Natured",
        "origin": "England",
        "lifespan": "6-10 years",
        "weight": "120-200+ lbs",
        "height": "27-32 inches",
        "care_level": "Moderate",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1631651537923-38d1e53424e1",
        "description": "Mastiffs are courageous, dignified, and good-natured gentle giants with a protective nature.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat"],
        "breed_group": "Working"
    },
    {
        "name": "Collie",
        "size": "Large",
        "temperament": "Devoted, Graceful, Proud",
        "origin": "Scotland",
        "lifespan": "12-14 years",
        "weight": "50-75 lbs",
        "height": "22-26 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1731147978145-4e2b2ff94cf7",
        "description": "Collies are devoted, graceful, and proud herding dogs famous for their loyalty and intelligence.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Bloat"],
        "breed_group": "Herding"
    }
]

# Combine all breeds
ALL_BREEDS = DOG_BREEDS_DATA + ADDITIONAL_BREEDS

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Welcome to the Dog Breeds API"}

@api_router.get("/breeds", response_model=List[DogBreed])
async def get_all_breeds():
    """Get all dog breeds"""
    breeds = await db.dog_breeds.find().to_list(1000)
    if not breeds:
        # If no breeds in database, populate with initial data
        await populate_breeds()
        breeds = await db.dog_breeds.find().to_list(1000)
    return [DogBreed(**breed) for breed in breeds]

@api_router.get("/breeds/{breed_id}", response_model=DogBreed)
async def get_breed_by_id(breed_id: str):
    """Get a specific breed by ID"""
    breed = await db.dog_breeds.find_one({"id": breed_id})
    if not breed:
        raise HTTPException(status_code=404, detail="Breed not found")
    return DogBreed(**breed)

@api_router.get("/breeds/search/{query}")
async def search_breeds(query: str):
    """Search breeds by name, temperament, or breed group"""
    breeds = await db.dog_breeds.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"temperament": {"$regex": query, "$options": "i"}},
            {"breed_group": {"$regex": query, "$options": "i"}},
            {"size": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(1000)
    return [DogBreed(**breed) for breed in breeds]

@api_router.post("/breeds/populate")
async def populate_breeds():
    """Populate the database with initial breed data"""
    # Clear existing data
    await db.dog_breeds.delete_many({})
    
    # Insert all breeds
    breed_objects = []
    for breed_data in ALL_BREEDS:
        breed_obj = DogBreed(**breed_data)
        breed_objects.append(breed_obj.dict())
    
    await db.dog_breeds.insert_many(breed_objects)
    return {"message": f"Successfully populated {len(breed_objects)} dog breeds"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()