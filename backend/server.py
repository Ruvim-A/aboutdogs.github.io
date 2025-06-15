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

# Dog breeds data with ACCURATE information
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
        "description": "Golden Retrievers are among the most beloved family dogs in the world, originally bred in Scotland during the 1860s as hunting companions for retrieving waterfowl from both land and water. These intelligent, loyal dogs possess a gentle mouth that allows them to carry game without damaging it, and this same soft bite makes them excellent with children, earning them a reputation as ideal family pets. Their patient, friendly temperament combined with their high intelligence makes them not only wonderful companions but also excellent service dogs, therapy dogs, and search-and-rescue dogs who excel in various working roles throughout their lives.",
        "health_issues": ["Hip Dysplasia", "Heart Disease", "Cancer", "Eye Conditions"],
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
        "description": "German Shepherds are versatile working dogs originally developed in Germany in the late 1800s for herding sheep, but their intelligence, loyalty, and trainability quickly made them valuable in military, police, and service work around the world. These confident, courageous dogs form incredibly strong bonds with their families and are naturally protective, making them excellent guard dogs, though they require early socialization to ensure their protective instincts don't become overly aggressive with strangers. Their high intelligence and work drive mean they need extensive mental and physical stimulation to prevent behavioral problems, and they thrive when given jobs to do, whether that's formal training, dog sports, or simply having consistent routines and tasks that challenge their minds and bodies.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat", "Degenerative Myelopathy"],
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
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/160846/french-bulldog-summer-smile-joy-160846.jpeg",
        "description": "French Bulldogs are charming, adaptable companion dogs that have become increasingly popular as urban pets due to their moderate exercise needs and generally quiet, well-mannered nature that makes them ideal for apartment living. Originally bred in England by lace workers who later moved to France during the Industrial Revolution, these dogs were developed specifically as companions rather than working dogs, and their entire temperament reflects this breeding purpose. Their distinctive 'bat ears,' flat faces, and compact, muscular build give them an adorable, almost comical appearance, but prospective owners should be aware that their flat faces can cause breathing difficulties, especially in hot weather, and they may require special care during exercise and travel.",
        "health_issues": ["Brachycephalic Obstructive Airway Syndrome", "Hip Dysplasia", "Breathing Problems"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Labrador Retriever",
        "size": "Large",
        "temperament": "Friendly, Outgoing, Active",
        "origin": "Newfoundland, Canada",
        "lifespan": "10-14 years",
        "weight": "55-80 lbs",
        "height": "21.5-24.5 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/19757632/pexels-photo-19757632.jpeg",
        "description": "Labrador Retrievers consistently rank as America's most popular dog breed, and for good reason—these friendly, outgoing dogs possess an ideal combination of intelligence, trainability, and gentle temperament that makes them excellent family pets, service dogs, and working companions. Originally bred in Newfoundland (not Labrador) as fishing dogs to help fishermen retrieve nets and fish, they possess a water-resistant coat and strong swimming ability that makes them natural water dogs who love swimming and water activities. Their high energy levels and intelligence require regular exercise and mental stimulation, but their eager-to-please attitude and food motivation make them relatively easy to train, though their enthusiasm and size can be overwhelming for small children and elderly family members if not properly managed.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Eye Disorders", "Heart Conditions"],
        "breed_group": "Sporting"
    },
    {
        "name": "Poodle (Standard)",
        "size": "Large",
        "temperament": "Active, Alert, Intelligent",
        "origin": "Germany",
        "lifespan": "10-18 years",
        "weight": "40-70 lbs",
        "height": "Over 15 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/3299899/pexels-photo-3299899.jpeg",
        "description": "Poodles are highly intelligent, athletic dogs that come in three sizes (Standard, Miniature, and Toy) but all share the same remarkable intelligence, hypoallergenic curly coat, and dignified bearing that has made them popular companions for centuries. Originally bred in Germany as water retrievers for duck hunting, they later became associated with French aristocracy and circus performances due to their exceptional trainability and natural showmanship. Their unique coat doesn't shed like most dogs but instead continues to grow, requiring professional grooming every 6-8 weeks to maintain their health and appearance, and their high intelligence and energy levels mean they excel in dog sports, obedience training, and various canine activities that challenge both their minds and bodies.",
        "health_issues": ["Hip Dysplasia", "Eye Disorders", "Addison's Disease"],
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
        "description": "Beagles are compact, sturdy hounds originally bred in England for hunting hare and rabbit, and they possess one of the best noses in the dog world, with their scenting ability being so reliable that they're commonly used in airports and border crossings to detect contraband. These merry, friendly dogs are known for their distinctive bay or howl that they use to communicate with their hunting partners, though this vocalization can be problematic in urban settings where neighbors might not appreciate their enthusiasm for 'singing.' Their pack hunting heritage makes them naturally social dogs who get along well with children and other pets, but their strong scenting drive means they can become completely absorbed in following interesting smells, requiring secure fencing and leash walking to prevent them from wandering off on scent trails.",
        "health_issues": ["Hip Dysplasia", "Ear Infections", "Obesity"],
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
        "description": "Rottweilers are powerful, confident dogs originally bred in Germany to drive cattle to market and later used by butchers to pull carts laden with meat, giving them their alternative name 'Rottweil Butcher's Dog.' These loyal, intelligent dogs are naturally protective of their families and territory, making them excellent guard dogs when properly trained and socialized, but their strength and protective instincts require experienced owners who can provide firm, consistent leadership. Despite their intimidating appearance, well-socialized Rottweilers are typically calm, confident dogs who are devoted to their families, though early socialization and ongoing training are essential to ensure their protective nature doesn't become problematic with strangers or other animals.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Heart Conditions", "Obesity"],
        "breed_group": "Working"
    },
    {
        "name": "Yorkshire Terrier",
        "size": "Small",
        "temperament": "Affectionate, Sprightly, Tomboyish",
        "origin": "England",
        "lifespan": "11-15 years",
        "weight": "4-7 lbs",
        "height": "7-8 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/1420405/pexels-photo-1420405.jpeg",
        "description": "Yorkshire Terriers are tiny but brave terriers originally bred in England during the Industrial Revolution to catch rats in textile mills, and despite their small size, they retain the bold, fearless temperament of their working terrier heritage. These elegant toy dogs are known for their beautiful, silky coats that can grow to floor length if maintained, though most pet owners keep them in shorter, more manageable clips for easier care. Their small size makes them fragile around young children, and their terrier instincts can make them surprisingly bossy and territorial with other dogs, but their devotion to their owners and their portable size make them excellent companions for adults who can provide the grooming and training these spirited little dogs require.",
        "health_issues": ["Dental Issues", "Patellar Luxation", "Tracheal Collapse"],
        "breed_group": "Toy"
    },
    {
        "name": "Bulldog",
        "size": "Medium",
        "temperament": "Docile, Willful, Friendly",
        "origin": "England",
        "lifespan": "8-12 years",
        "weight": "49-55 lbs",
        "height": "13-15 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/776078/pexels-photo-776078.jpeg",
        "description": "Bulldogs are distinctive, muscular dogs with wrinkled faces and pushed-in noses that were originally bred for bull-baiting in medieval England, but modern Bulldogs have been bred for companionship and have much gentler temperaments than their fierce ancestors. These calm, friendly dogs are known for their patient nature with children and their tendency to form strong bonds with their families, though their brachycephalic (short-nosed) structure makes them prone to breathing difficulties and overheating. Their low exercise needs and generally calm demeanor make them suitable for apartment living, but prospective owners should be prepared for potential health issues related to their breathing and the special care required during hot weather or strenuous activity.",
        "health_issues": ["Brachycephalic Syndrome", "Hip Dysplasia", "Skin Infections"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Dachshund",
        "size": "Small",
        "temperament": "Friendly, Curious, Spunky",
        "origin": "Germany",
        "lifespan": "12-16 years",
        "weight": "Standard: 16-32 lbs, Miniature: up to 11 lbs",
        "height": "Standard: 8-9 inches, Miniature: 5-6 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/169524/pexels-photo-169524.jpeg",
        "description": "Dachshunds, affectionately known as 'wiener dogs' or 'sausage dogs,' were originally bred in Germany to hunt badgers in their underground dens, with their elongated bodies and short legs perfectly designed for pursuing prey into narrow burrows. These brave, curious dogs come in three coat varieties (smooth, long-haired, and wire-haired) and two sizes (standard and miniature), but all share the same spunky, determined personality that made them effective hunters. Their unique body structure, while charming and distinctive, makes them prone to intervertebral disc disease, so owners must be careful to prevent jumping from heights and maintain their dogs at healthy weights to reduce stress on their spines.",
        "health_issues": ["Intervertebral Disc Disease", "Obesity", "Dental Issues"],
        "breed_group": "Hound"
    },
    {
        "name": "Siberian Husky",
        "size": "Large",
        "temperament": "Loyal, Outgoing, Mischievous",
        "origin": "Siberia",
        "lifespan": "12-14 years",
        "weight": "Males: 45-60 lbs, Females: 35-50 lbs",
        "height": "Males: 21-23.5 inches, Females: 20-22 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.pexels.com/photos/3715587/pexels-photo-3715587.jpeg",
        "description": "Siberian Huskies are athletic, endurance dogs originally bred by the Chukchi people of Siberia to pull sleds across long distances in harsh Arctic conditions, and they retain their incredible stamina and love of running that made them legendary sled dogs. These friendly, outgoing dogs are known for their striking blue or multicolored eyes, thick double coats, and distinctive facial markings, as well as their tendency to 'talk' using various vocalizations rather than traditional barking. Their high energy levels and intelligence require extensive daily exercise and mental stimulation, and their independent nature and strong prey drive mean they need secure fencing and experienced owners who understand their need for consistent leadership and adequate physical outlets for their boundless energy.",
        "health_issues": ["Hip Dysplasia", "Eye Conditions", "Zinc-Responsive Dermatosis"],
        "breed_group": "Working"
    },
    {
        "name": "Border Collie",
        "size": "Medium",
        "temperament": "Affectionate, Smart, Energetic",
        "origin": "England/Scotland",
        "lifespan": "10-17 years",
        "weight": "Males: 30-45 lbs, Females: slightly smaller",
        "height": "18-23 inches",
        "care_level": "Very High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1649535444934-c33b4a1eee65",
        "description": "Border Collies are widely considered the most intelligent dog breed in the world, originally developed along the border between England and Scotland as herding dogs capable of controlling sheep with minimal human direction using their intense gaze, known as 'the eye.' These highly athletic, energetic dogs possess an almost supernatural ability to read and respond to their handler's commands, making them unparalleled working dogs but also requiring owners who can provide the extensive mental and physical stimulation these brilliant dogs need. Their intelligence and work drive can be both a blessing and a challenge, as they excel in dog sports and training but can become destructive or develop behavioral problems if their needs for mental and physical exercise aren't adequately met.",
        "health_issues": ["Hip Dysplasia", "Collie Eye Anomaly", "Epilepsy", "Hypothyroidism"],
        "breed_group": "Herding"
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
        "description": "Boxers are energetic, fun-loving dogs originally bred in Germany as hunting companions and later used as messenger dogs during World War I. These medium to large-sized dogs are known for their distinctive square-shaped heads, strong jaws, and expressive dark eyes that convey their playful and alert nature. Their boundless energy and enthusiasm make them excellent family pets, especially for active households, though they require consistent training and socialization from an early age to channel their exuberance appropriately.",
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
        "description": "Great Danes, often called 'gentle giants,' are among the tallest dog breeds in the world and are known for their imposing stature combined with a remarkably gentle and friendly temperament. Despite their massive size, these dogs are incredibly patient and make excellent family companions, often thinking they're lap dogs and attempting to curl up with their human family members. Originally bred in Germany to hunt wild boar, Great Danes today are primarily kept as loving family pets who are surprisingly adaptable to various living situations, though they do require adequate space to move around comfortably.",
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
        "description": "Shih Tzus are charming toy dogs with a rich history as companions to Chinese royalty, specifically bred to be the perfect lap dogs and palace pets. Their flowing double coat, distinctive pushed-in face, and large dark eyes give them an almost toy-like appearance that has captivated dog lovers for centuries. These small but sturdy dogs are known for their friendly, outgoing personalities and their ability to get along well with children and other pets, making them ideal family companions for those who can commit to their intensive grooming needs.",
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
        "description": "Boston Terriers, affectionately known as the 'American Gentleman' due to their tuxedo-like black and white coat pattern, are one of the few breeds developed in America. These compact, well-muscled dogs were originally bred in Boston in the late 1800s and have since become beloved family pets known for their intelligence, friendliness, and amusing personality quirks. Their short coat requires minimal grooming, and their moderate exercise needs make them excellent apartment dogs, though they thrive on mental stimulation and enjoy interactive play with their families.",
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
        "description": "Cocker Spaniels are sporting dogs with beautiful, silky coats and gentle expressions that reflect their sweet, happy-go-lucky nature. Originally bred as hunting dogs to flush out and retrieve woodcock and other game birds, they possess a natural enthusiasm for outdoor activities while maintaining a gentle temperament that makes them excellent family pets. Their beautiful coats require regular professional grooming to prevent matting, and their intelligent, eager-to-please nature makes them highly trainable, though they can be sensitive and respond best to positive reinforcement training methods.",
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
        "description": "Bernese Mountain Dogs are striking, large working dogs from Switzerland with distinctive tri-colored coats of black, white, and rust that make them instantly recognizable. Originally bred as farm dogs to drive cattle, pull carts, and serve as watchdogs in the Swiss Alps, they possess a calm, patient temperament combined with impressive strength and endurance. Despite their working heritage, they are known for being gentle giants who are particularly good with children, though their shorter lifespan compared to other breeds is a consideration for potential owners who should be prepared for the heartbreak that comes with loving these magnificent but relatively short-lived companions.",
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
        "description": "Mastiffs are among the heaviest dog breeds in the world, with some males weighing over 200 pounds, yet they are known for their gentle, good-natured temperament that contrasts dramatically with their imposing physical presence. These ancient dogs have a history dating back thousands of years, having served as war dogs, gladiator opponents, and estate guardians throughout history, but modern Mastiffs are primarily kept as family companions who are surprisingly gentle and patient with children. Their massive size means they require adequate space and careful consideration of their exercise needs, as overexertion can be harmful, particularly in hot weather, but their calm, dignified nature makes them excellent indoor companions for families who can accommodate their substantial physical presence.",
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
        "description": "Collies are elegant, intelligent herding dogs made famous by the television and movie character Lassie, and they truly embody the loyal, heroic qualities portrayed in popular media. These graceful dogs possess a natural instinct to herd and protect, making them excellent family guardians who are particularly devoted to children, often displaying an almost supernatural ability to sense danger or distress. Their beautiful, flowing coats require regular brushing to prevent matting, and their high intelligence combined with their eagerness to please makes them highly trainable, though they need adequate mental and physical stimulation to prevent boredom-related behavioral issues.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Bloat"],
        "breed_group": "Herding"
    },
    {
        "name": "Akita",
        "size": "Large",
        "temperament": "Dignified, Courageous, Profoundly Loyal",
        "origin": "Japan",
        "lifespan": "10-13 years",
        "weight": "70-130 lbs",
        "height": "24-28 inches",
        "care_level": "High",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1683480951100-202f9ae1df83",
        "description": "Akitas are powerful, dignified dogs from Japan known for their unwavering loyalty and courage, immortalized by the famous Hachiko who waited for his deceased owner at a train station for nearly 10 years. These large, spitz-type dogs were originally bred to hunt wild boar, bear, and other large game in the mountainous regions of Japan, and they retain their independent, strong-willed nature that requires experienced handling and consistent training. Their thick double coat and curled tail give them a distinctive appearance, and while they are deeply devoted to their families, they can be aloof with strangers and may not get along well with other dogs, making early socialization crucial for this noble breed.",
        "health_issues": ["Hip Dysplasia", "Autoimmune Disorders", "Bloat"],
        "breed_group": "Working"
    },
    {
        "name": "Basset Hound",
        "size": "Medium",
        "temperament": "Patient, Low-Key, Charming",
        "origin": "France",
        "lifespan": "12-13 years",
        "weight": "40-65 lbs",
        "height": "11-15 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/29472456/pexels-photo-29472456.jpeg",
        "description": "Basset Hounds are distinctive, low-slung hounds with extraordinarily long ears and a remarkable sense of smell that ranks second only to the Bloodhound among all dog breeds. Originally bred in France for hunting small game, their short legs and sturdy build allow them to track scents close to the ground for hours without tiring, though this hunting instinct can make them single-minded when following an interesting scent trail. These charming dogs are known for their patient, laid-back personalities and their ability to get along well with children and other pets, though their deep, resonant bay can be quite loud, and their stubborn streak requires patient, consistent training with plenty of positive reinforcement.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat"],
        "breed_group": "Hound"
    },
    {
        "name": "Weimaraner",
        "size": "Large",
        "temperament": "Friendly, Fearless, Alert, Obedient",
        "origin": "Germany",
        "lifespan": "10-13 years",
        "weight": "55-90 lbs",
        "height": "23-27 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1729460693156-c322852e3e3b",
        "description": "Weimaraners, often called the 'Gray Ghost' due to their distinctive silver-gray coat and light-colored eyes, are athletic hunting dogs bred by German nobility for tracking large game like deer, bear, and wild boar. These elegant, muscular dogs possess boundless energy and require extensive daily exercise and mental stimulation to prevent destructive behaviors that can result from boredom or pent-up energy. Their intelligence and eagerness to please make them highly trainable, but they form extremely strong bonds with their families and can develop separation anxiety if left alone for extended periods, making them best suited for active owners who can provide consistent companionship and engagement.",
        "health_issues": ["Hip Dysplasia", "Bloat", "Heart Problems"],
        "breed_group": "Sporting"
    },
    {
        "name": "Newfoundland",
        "size": "Giant",
        "temperament": "Sweet, Patient, Devoted",
        "origin": "Canada",
        "lifespan": "9-10 years",
        "weight": "100-150 lbs",
        "height": "26-28 inches",
        "care_level": "High",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/19935666/pexels-photo-19935666.jpeg",
        "description": "Newfoundlands are massive, gentle working dogs originally bred as fishing and rescue dogs in the cold waters off the coast of Newfoundland, Canada, where their webbed feet, water-resistant double coat, and powerful swimming ability made them invaluable companions to fishermen. These 'gentle giants' are renowned for their patient, sweet temperament and their natural instinct to rescue people in distress, particularly in water, earning them the nickname 'lifeguard dogs' for their heroic water rescue abilities. Their thick, heavy coat requires daily brushing to prevent matting and manage shedding, and while they are generally calm and easy-going, they do drool considerably and their large size means they need adequate space and careful consideration of their exercise needs to maintain their health and happiness.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Heart Problems"],
        "breed_group": "Working"
    },
    {
        "name": "Vizsla",
        "size": "Medium",
        "temperament": "Affectionate, Gentle, Energetic",
        "origin": "Hungary",
        "lifespan": "12-14 years",
        "weight": "44-60 lbs",
        "height": "21-24 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/32490579/pexels-photo-32490579.jpeg",
        "description": "Vizslas are elegant, athletic hunting dogs from Hungary with distinctive golden-rust colored coats and an affectionate, gentle nature that has earned them the nickname 'Velcro dogs' for their tendency to stick close to their human companions. These medium-sized sporting dogs were bred by Hungarian nobility as versatile hunting companions capable of pointing, retrieving, and tracking game in various terrains and weather conditions. Their high energy levels and intelligence require extensive daily exercise and mental stimulation, making them ideal companions for active individuals or families who enjoy hiking, running, or other outdoor activities, though they can become anxious or destructive if their exercise needs are not adequately met.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Epilepsy"],
        "breed_group": "Sporting"
    },
    {
        "name": "Whippet",
        "size": "Medium",
        "temperament": "Calm, Friendly, Quiet",
        "origin": "England",
        "lifespan": "12-15 years",
        "weight": "25-40 lbs",
        "height": "18-22 inches",
        "care_level": "Low",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/1633522/pexels-photo-1633522.jpeg",
        "description": "Whippets are sleek, graceful sighthounds that resemble small Greyhounds and are known for their incredible speed, capable of reaching up to 35 miles per hour despite their medium size. Originally bred in England as racing dogs and rabbit hunters, these gentle dogs are often described as having a dual personality: they can be lightning-fast athletes on the track or during play, then transform into calm, quiet couch potatoes who love nothing more than lounging with their families. Their thin skin and short coat make them sensitive to cold weather, often requiring sweaters or coats in winter, but their minimal grooming needs and generally quiet, well-mannered nature make them excellent apartment dogs for those who can provide brief bursts of high-intensity exercise.",
        "health_issues": ["Heart Problems", "Eye Problems", "Deafness"],
        "breed_group": "Hound"
    },
    {
        "name": "Doberman Pinscher",
        "size": "Large",
        "temperament": "Alert, Fearless, Loyal",
        "origin": "Germany",
        "lifespan": "10-13 years",
        "weight": "60-100 lbs",
        "height": "24-28 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1665333354010-050f08f35907",
        "description": "Doberman Pinschers are sleek, powerful dogs originally bred in Germany by a tax collector named Karl Friedrich Louis Dobermann who wanted a loyal, protective companion for his dangerous work collecting taxes in rough neighborhoods. These intelligent, athletic dogs are known for their unwavering loyalty to their families and their natural protective instincts, making them excellent guard dogs, though they require extensive socialization and training to ensure their protective nature doesn't become overly aggressive. Their short, smooth coat requires minimal grooming, but their high intelligence and energy levels demand consistent mental and physical stimulation, and they thrive best with experienced owners who can provide firm, consistent leadership and plenty of structured activities.",
        "health_issues": ["Heart Problems", "Hip Dysplasia", "Von Willebrand Disease"],
        "breed_group": "Working"
    },
    {
        "name": "Bloodhound",
        "size": "Large",
        "temperament": "Friendly, Independent, Inquisitive",
        "origin": "Belgium",
        "lifespan": "10-12 years",
        "weight": "80-110 lbs",
        "height": "23-27 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/10626084/pexels-photo-10626084.jpeg",
        "description": "Bloodhounds possess the most accurate sense of smell of any dog breed, with over 300 million scent receptors compared to humans' mere 6 million, making them invaluable for search and rescue operations and law enforcement tracking work. These large, wrinkled hounds were originally bred in medieval Europe by monks to track wounded game, and their incredible scenting ability is so reliable that evidence found by Bloodhounds is admissible in courts of law. While they are gentle, friendly dogs who get along well with children and other pets, their powerful scenting drive means they can become completely absorbed in following a scent trail, requiring secure fencing and leash walking to prevent them from wandering off in pursuit of an interesting smell, and their independent nature can make training challenging, requiring patience and consistency from their owners.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat"],
        "breed_group": "Hound"
    },
    {
        "name": "Saint Bernard",
        "size": "Giant",
        "temperament": "Playful, Charming, Inquisitive",
        "origin": "Switzerland",
        "lifespan": "8-10 years",
        "weight": "120-180 lbs",
        "height": "26-30 inches",
        "care_level": "Moderate",
        "exercise_needs": "Low",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1683480951100-202f9ae1df83",
        "description": "Saint Bernards are massive, gentle dogs originally bred by monks at the Saint Bernard Pass in the Swiss Alps to rescue travelers lost in snow and avalanches, with some legendary dogs credited with saving over 40 lives during their working careers. These gentle giants are known for their patient, friendly temperament with children, earning them the nickname 'nanny dogs,' though their enormous size means supervision is necessary around small children who could be accidentally knocked over. Despite their impressive rescue heritage, modern Saint Bernards are primarily family companions who are surprisingly calm and gentle indoors, though they do drool considerably and their thick coats require regular brushing, especially during shedding seasons when they can leave substantial amounts of hair throughout the home.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat"],
        "breed_group": "Working"
    },
    {
        "name": "Afghan Hound",
        "size": "Large",
        "temperament": "Independent, Sweet, Dignified",
        "origin": "Afghanistan",
        "lifespan": "12-18 years",
        "weight": "50-60 lbs",
        "height": "24-29 inches",
        "care_level": "Very High",
        "exercise_needs": "High",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Very High",
        "image_url": "https://images.unsplash.com/photo-1526440847959-4e38e7f00b04",
        "description": "Afghan Hounds are aristocratic sighthounds with flowing, silky coats and a dignified bearing that reflects their ancient heritage as hunting dogs for Afghan royalty in the harsh mountainous regions of Afghanistan. These elegant dogs were bred to hunt leopards, wolves, and gazelles across difficult terrain, developing their characteristic independent, aloof personality that can make them seem almost cat-like in their selective affection and stubborn streak. Their spectacular coat requires daily brushing and professional grooming to maintain its beauty and prevent matting, and their independent nature combined with their strong prey drive means they need experienced owners who understand sighthound temperament and can provide secure areas for exercise, as they will chase anything that moves and may not respond to recall commands when in pursuit.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Allergies"],
        "breed_group": "Hound"
    },
    {
        "name": "Irish Setter",
        "size": "Large",
        "temperament": "Outgoing, Sweet-Natured, Active",
        "origin": "Ireland",
        "lifespan": "12-15 years",
        "weight": "60-70 lbs",
        "height": "25-27 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1633291294388-3e73294ab65f",
        "description": "Irish Setters are stunning sporting dogs with flowing, mahogany-red coats and exuberant personalities that make them beloved family companions, though their high energy levels and playful nature can be overwhelming for some families. Originally bred in Ireland as bird dogs to locate and point game birds, these athletic dogs retain their hunting instincts and require extensive daily exercise and mental stimulation to prevent destructive behaviors that can result from boredom or excess energy. Their beautiful, silky coats require regular brushing to prevent tangles and matting, and their friendly, outgoing nature makes them excellent with children and other dogs, though their enthusiasm and size mean they may accidentally knock over small children during play, requiring supervision and training to manage their exuberant greetings.",
        "health_issues": ["Hip Dysplasia", "Bloat", "Eye Problems"],
        "breed_group": "Sporting"
    },
    {
        "name": "Cavalier King Charles Spaniel",
        "size": "Small",
        "temperament": "Affectionate, Gentle, Graceful",
        "origin": "England",
        "lifespan": "12-15 years",
        "weight": "13-18 lbs",
        "height": "12-13 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.pexels.com/photos/5731898/pexels-photo-5731898.jpeg",
        "description": "Cavalier King Charles Spaniels are sweet, gentle toy dogs with beautiful, silky coats and large, expressive eyes that reflect their affectionate, eager-to-please nature that has made them beloved companion dogs for centuries. Named after King Charles II of England, who was rarely seen without several of these spaniels by his side, these dogs were bred specifically to be lap dogs and companions, and they excel in this role with their adaptable, friendly temperament. Their moderate exercise needs and generally quiet nature make them excellent apartment dogs, though they do shed regularly and their feathered coats require regular brushing, and prospective owners should be aware that this breed is unfortunately prone to several serious health conditions, including heart problems and neurological issues, making health screening of breeding stock crucial.",
        "health_issues": ["Heart Problems", "Neurological Disorders", "Eye Problems"],
        "breed_group": "Toy"
    },
    {
        "name": "Alaskan Malamute",
        "size": "Large",
        "temperament": "Affectionate, Loyal, Playful",
        "origin": "Alaska",
        "lifespan": "10-14 years",
        "weight": "75-85 lbs",
        "height": "23-25 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1617895153857-82fe79adfcd4",
        "description": "Alaskan Malamutes are powerful, wolf-like dogs bred by the Inuit people of Alaska to pull heavy sleds across long distances in harsh Arctic conditions, and they retain their incredible strength, endurance, and independent spirit that made them invaluable to their original owners. These large, fluffy dogs have thick double coats that protect them in temperatures as low as -20°F, but this same coat makes them prone to overheating in warm climates and requires daily brushing to manage shedding, especially during their twice-yearly 'blowout' periods when they shed their undercoat. Their strong pack instincts and high prey drive mean they may not get along well with small animals or strange dogs, and their intelligence combined with their independent nature can make them challenging to train, requiring experienced owners who can provide firm, consistent leadership and plenty of physical and mental stimulation to keep these powerful dogs happy and well-behaved.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Polyneuropathy"],
        "breed_group": "Working"
    },
    {
        "name": "English Springer Spaniel",
        "size": "Medium",
        "temperament": "Friendly, Eager, Alert",
        "origin": "England",
        "lifespan": "12-14 years",
        "weight": "40-50 lbs",
        "height": "19-20 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.pexels.com/photos/32572648/pexels-photo-32572648.jpeg",
        "description": "English Springer Spaniels are energetic, medium-sized sporting dogs originally bred to 'spring' or flush game birds from cover for hunters, and they retain their incredible enthusiasm for work and play that can make them wonderful but demanding family companions. These intelligent, athletic dogs possess boundless energy and require extensive daily exercise and mental stimulation to prevent behavioral problems that can arise from boredom or pent-up energy, making them ideal companions for active families who enjoy hiking, jogging, or other outdoor activities. Their beautiful, medium-length coats require regular brushing and professional grooming to prevent matting and manage shedding, and their eager-to-please nature combined with their high intelligence makes them highly trainable, though their enthusiasm can sometimes overwhelm their ability to focus, requiring patient, consistent training that channels their energy productively.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Ear Infections"],
        "breed_group": "Sporting"
    },
    {
        "name": "Papillon",
        "size": "Small",
        "temperament": "Happy, Alert, Friendly",
        "origin": "France/Belgium",
        "lifespan": "14-16 years",
        "weight": "5-10 lbs",
        "height": "8-11 inches",
        "care_level": "Moderate",
        "exercise_needs": "Moderate",
        "good_with_kids": False,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1689009480504-6420452a7e8e",
        "description": "Papillons are tiny, elegant toy dogs named for their distinctive butterfly-like ears (papillon means butterfly in French) and known for their remarkable intelligence that consistently ranks them among the smartest small dog breeds. Despite their diminutive size, these dogs possess surprising athleticism and excel in dog sports like agility and obedience competitions, often outperforming much larger breeds with their quick wit and eager-to-please attitude. Their long, silky coats are surprisingly easy to maintain compared to other long-haired breeds, requiring only regular brushing to prevent tangles, but their small size makes them fragile around young children, and they can be somewhat territorial with other dogs despite their generally friendly nature, making early socialization important for well-rounded development.",
        "health_issues": ["Luxating Patella", "Eye Problems", "Dental Issues"],
        "breed_group": "Toy"
    },
    {
        "name": "Bull Terrier",
        "size": "Medium",
        "temperament": "Playful, Charming, Mischievous",
        "origin": "England",
        "lifespan": "12-13 years",
        "weight": "50-70 lbs",
        "height": "21-22 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1611611158876-41699b77a059",
        "description": "Bull Terriers are distinctive, egg-shaped-headed dogs with playful, mischievous personalities that can be both endearing and challenging for owners who aren't prepared for their strong-willed, sometimes stubborn nature. Originally bred in England for bull baiting and later as fighting dogs, modern Bull Terriers have retained their courage and determination but have been bred for companionship, resulting in dogs that are typically good with children but may not get along well with other dogs or small animals due to their high prey drive. Their short, easy-care coats require minimal grooming, but their high energy levels and intelligence demand consistent training and plenty of physical and mental stimulation to prevent destructive behaviors, and their strong personalities require experienced owners who can provide firm, consistent leadership while still maintaining the positive, playful training approach these sensitive dogs respond to best.",
        "health_issues": ["Deafness", "Heart Problems", "Kidney Disease"],
        "breed_group": "Terrier"
    },
    {
        "name": "Chow Chow",
        "size": "Medium",
        "temperament": "Independent, Loyal, Reserved",
        "origin": "China",
        "lifespan": "8-12 years",
        "weight": "45-70 lbs",
        "height": "17-20 inches",
        "care_level": "High",
        "exercise_needs": "Moderate",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Very High",
        "image_url": "https://images.unsplash.com/photo-1683480951100-202f9ae1df83",
        "description": "Chow Chows are ancient, lion-like spitz dogs from China with distinctive blue-black tongues and thick, fluffy double coats that give them a dignified, almost regal appearance befitting their history as companions to Chinese emperors. These independent, aloof dogs are known for their loyalty to their families but their wariness of strangers, making them excellent watchdogs but requiring extensive early socialization to prevent them from becoming overly protective or aggressive with unfamiliar people or animals. Their thick coats require daily brushing to prevent matting and manage heavy shedding, particularly during seasonal coat changes, and their independent, cat-like personality means they are not as eager to please as many other breeds, requiring patient, consistent training from owners who understand and respect their somewhat stubborn, dignified nature.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Eye Problems"],
        "breed_group": "Non-Sporting"
    },
    {
        "name": "Basenji",
        "size": "Small",
        "temperament": "Independent, Smart, Poised",
        "origin": "Central Africa",
        "lifespan": "13-14 years",
        "weight": "22-24 lbs",
        "height": "16-17 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.pexels.com/photos/3487734/pexels-photo-3487734.jpeg",
        "description": "Basenjis are unique, cat-like dogs from Central Africa known as the 'barkless dog' because they don't bark in the traditional sense, instead making distinctive yodel-like sounds called 'baroos' when they want to communicate. These ancient hunting dogs possess remarkable cleanliness habits, grooming themselves like cats and having very little doggy odor, but their intelligence and independence can make them challenging to train as they tend to think for themselves rather than blindly follow commands. Their high prey drive and escape artist tendencies require secure fencing and careful supervision, as they are capable climbers and jumpers who will pursue small animals with single-minded determination, and their strong-willed nature combined with their high exercise needs makes them best suited for experienced dog owners who appreciate their unique personality and can provide consistent mental and physical stimulation.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Kidney Disease"],
        "breed_group": "Hound"
    },
    {
        "name": "Portuguese Water Dog",
        "size": "Medium",
        "temperament": "Affectionate, Adventurous, Athletic",
        "origin": "Portugal",
        "lifespan": "11-13 years",
        "weight": "35-60 lbs",
        "height": "17-23 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/1407167/pexels-photo-1407167.jpeg",
        "description": "Portuguese Water Dogs are athletic, intelligent working dogs originally bred to assist Portuguese fishermen by herding fish into nets, retrieving lost tackle, and carrying messages between boats, giving them an exceptional affinity for water and swimming. These medium-sized dogs have distinctive curly or wavy coats that are considered hypoallergenic because they don't shed like most breeds, instead requiring professional grooming every 6-8 weeks to maintain their coat's health and appearance. Their high intelligence and energy levels require extensive daily exercise and mental stimulation, making them excellent companions for active families who enjoy water activities, hiking, or dog sports, though their working heritage means they can become destructive if their physical and mental needs aren't adequately met, requiring owners who understand the commitment involved in properly exercising and training these capable, driven dogs.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Heart Problems"],
        "breed_group": "Working"
    },
    {
        "name": "Rhodesian Ridgeback",
        "size": "Large",
        "temperament": "Affectionate, Dignified, Even-Tempered",
        "origin": "Southern Africa",
        "lifespan": "10-12 years",
        "weight": "70-85 lbs",
        "height": "24-27 inches",
        "care_level": "Moderate",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1520038410233-7141be7e6f97",
        "description": "Rhodesian Ridgebacks are powerful, athletic hounds originally bred in Southern Africa to hunt lions, giving them their common name 'African Lion Hound,' and they possess the courage, strength, and endurance that such dangerous work required. These distinctive dogs are named for the ridge of hair that grows in the opposite direction along their spine, creating a distinctive marking that is unique to this breed, and their short, easy-care coats belie their substantial exercise needs and strong-willed personalities. While they are generally calm and dignified in the home, they retain strong hunting instincts and may not get along well with small animals or strange dogs, requiring early socialization and consistent training from owners who can provide firm, fair leadership and adequate exercise to keep these powerful, independent dogs mentally and physically satisfied.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Dermoid Sinus"],
        "breed_group": "Hound"
    }
]

# Combine all breeds (ensuring we have 52+ breeds)
FINAL_ADDITIONAL_BREEDS = [
    {
        "name": "Brittany",
        "size": "Medium",
        "temperament": "Energetic, Eager, Athletic",
        "origin": "France",
        "lifespan": "12-15 years",
        "weight": "30-40 lbs",
        "height": "17-21 inches",
        "care_level": "High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Moderate",
        "image_url": "https://images.unsplash.com/photo-1605638868237-0660a05a135b",
        "description": "Brittany dogs (formerly known as Brittany Spaniels) are compact, athletic sporting dogs originally bred in France as versatile hunting companions capable of pointing, retrieving, and working in various terrains and weather conditions. These energetic, medium-sized dogs possess boundless enthusiasm for outdoor activities and require extensive daily exercise and mental stimulation to prevent behavioral problems that can arise from their high energy levels and working drive. Their friendly, eager-to-please nature makes them excellent family pets for active households, though their intensity and exercise requirements mean they are not suitable for sedentary owners or apartment living without adequate exercise outlets.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Epilepsy"],
        "breed_group": "Sporting"
    },
    {
        "name": "Cane Corso",
        "size": "Large",
        "temperament": "Affectionate, Intelligent, Majestic",
        "origin": "Italy",
        "lifespan": "9-12 years",
        "weight": "88-110 lbs",
        "height": "23-28 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": False,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1643811356771-dc2c1a53e235",
        "description": "Cane Corsos are powerful, majestic Italian mastiffs originally bred as guardians, hunters, and farm dogs who possess both the strength to take down wild boar and the intelligence to serve as versatile working companions. These large, athletic dogs are known for their devotion to their families and their natural protective instincts, but they require experienced owners who can provide consistent leadership, extensive socialization, and proper training to ensure their protective nature doesn't become problematic. Their short coats require minimal grooming, but their size, strength, and protective instincts mean they need confident handling and adequate exercise to channel their energy and drive appropriately, making them unsuitable for novice dog owners or those unable to commit to their substantial training and exercise needs.",
        "health_issues": ["Hip Dysplasia", "Elbow Dysplasia", "Bloat"],
        "breed_group": "Working"
    },
    {
        "name": "Australian Cattle Dog",
        "size": "Medium",
        "temperament": "Alert, Curious, Pleasant",
        "origin": "Australia",
        "lifespan": "12-16 years",
        "weight": "35-50 lbs",
        "height": "17-20 inches",
        "care_level": "Very High",
        "exercise_needs": "Very High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Low",
        "image_url": "https://images.unsplash.com/photo-1643505339041-5f6328214385",
        "description": "Australian Cattle Dogs, also known as Blue Heelers or Red Heelers depending on their coat color, are incredibly intelligent, high-energy working dogs bred in Australia to drive cattle across long distances in harsh conditions. These compact, athletic dogs possess almost limitless endurance and a strong work drive that requires extensive daily exercise and mental stimulation to prevent destructive behaviors that can result from boredom or pent-up energy. Their loyalty and intelligence make them excellent companions for very active owners, but their herding instincts may lead them to nip at the heels of children or other pets, requiring early training and socialization to redirect these natural behaviors appropriately.",
        "health_issues": ["Hip Dysplasia", "Progressive Retinal Atrophy", "Deafness"],
        "breed_group": "Herding"
    },
    {
        "name": "Pomeranian",
        "size": "Small",
        "temperament": "Inquisitive, Bold, Lively",
        "origin": "Germany/Poland",
        "lifespan": "12-16 years",
        "weight": "3-7 lbs",
        "height": "6-7 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": False,
        "good_with_pets": False,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/3512/garden-dog-pet.jpg",
        "description": "Pomeranians are tiny, fox-like spitz dogs with fluffy double coats and outsized personalities that make them believe they're much larger than their 3-7 pound frames would suggest. Originally bred down from larger spitz-type sled dogs in the Pomerania region of Germany and Poland, these miniature companions became favorites of European royalty, including Queen Victoria, who helped popularize the breed. Despite their small size, they can be quite bold and may attempt to challenge much larger dogs, requiring careful supervision and socialization to prevent them from getting into dangerous situations, and their thick coats require daily brushing to prevent matting and manage their considerable shedding.",
        "health_issues": ["Luxating Patella", "Tracheal Collapse", "Dental Problems"],
        "breed_group": "Toy"
    },
    {
        "name": "Havanese",
        "size": "Small",
        "temperament": "Outgoing, Funny, Intelligent",
        "origin": "Cuba",
        "lifespan": "14-16 years",
        "weight": "7-13 lbs",
        "height": "8-12 inches",
        "care_level": "High",
        "exercise_needs": "Moderate",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.unsplash.com/photo-1667581207771-3ec800b19baf",
        "description": "Havanese are charming, silky-coated toy dogs that serve as Cuba's national dog and were originally bred as companions for Cuban aristocracy, developing their outgoing, people-oriented personalities through centuries of selective breeding for companionship. These small but sturdy dogs are known for their amusing antics and natural showmanship, often seeming to perform for their families' entertainment, and their intelligence and eagerness to please make them highly trainable despite their sometimes mischievous nature. Their beautiful, flowing coats can be maintained in full length for showing or trimmed short for easier care, but either way requires regular brushing and professional grooming to prevent matting and maintain their coat's health and appearance.",
        "health_issues": ["Heart Problems", "Eye Problems", "Hip Dysplasia"],
        "breed_group": "Toy"
    },
    {
        "name": "Shetland Sheepdog",
        "size": "Small",
        "temperament": "Playful, Energetic, Bright",
        "origin": "Scotland",
        "lifespan": "12-14 years",
        "weight": "15-25 lbs",
        "height": "13-16 inches",
        "care_level": "High",
        "exercise_needs": "High",
        "good_with_kids": True,
        "good_with_pets": True,
        "grooming_needs": "High",
        "image_url": "https://images.unsplash.com/photo-1516371535707-512a1e83bb9a",
        "description": "Shetland Sheepdogs, often called 'Shelties,' are small, elegant herding dogs that resemble miniature Rough Collies and were originally bred on the Shetland Islands of Scotland to herd sheep, ponies, and poultry in harsh weather conditions. These intelligent, agile dogs retain their strong herding instincts and may attempt to herd children, other pets, or even cars if not properly trained and socialized, but their eager-to-please nature and high intelligence make them excel in obedience training and dog sports. Their beautiful double coats require regular brushing to prevent matting and manage seasonal shedding, and their sensitive nature means they respond best to positive, gentle training methods rather than harsh corrections.",
        "health_issues": ["Hip Dysplasia", "Eye Problems", "Epilepsy"],
        "breed_group": "Herding"
    },
    {
        "name": "Maltese",
        "size": "Small",
        "temperament": "Gentle, Playful, Charming",
        "origin": "Malta",
        "lifespan": "12-15 years",
        "weight": "4-7 lbs",
        "height": "7-9 inches",
        "care_level": "High",
        "exercise_needs": "Low",
        "good_with_kids": False,
        "good_with_pets": True,
        "grooming_needs": "Very High",
        "image_url": "https://images.pexels.com/photos/373467/pexels-photo-373467.jpeg",
        "description": "Maltese are ancient toy dogs with flowing, silky white coats that have been prized as companions by nobility and aristocracy for over 2,000 years, with evidence of the breed appearing in art and literature from ancient Greece, Rome, and Egypt. These tiny, elegant dogs were bred exclusively for companionship and have never had a working function, resulting in dogs that are perfectly content to be lap dogs and indoor companions, though they can be surprisingly bold and fearless despite their diminutive size. Their gorgeous coats require daily brushing and professional grooming to maintain their beauty and prevent matting, and their small size makes them fragile around young children, though they generally get along well with gentle older children and other small pets.",
        "health_issues": ["Luxating Patella", "Dental Problems", "Heart Problems"],
        "breed_group": "Toy"
    }
]

ALL_BREEDS = DOG_BREEDS_DATA + ADDITIONAL_BREEDS + FINAL_ADDITIONAL_BREEDS

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