"""
Rental Property Expense Estimation Framework

Based on industry research and best practices for 2024-2025.
Provides data-driven estimates for maintenance, vacancy, management, and other expenses.
"""

from typing import Dict, List, Tuple, NamedTuple
from enum import Enum
import math

class PropertyType(Enum):
    SINGLE_FAMILY = "single_family"
    DUPLEX = "duplex"
    MULTIFAMILY = "multifamily"
    CONDO_TOWNHOME = "condo_townhome"

class PropertyAge(Enum):
    NEW = "new"          # 0-5 years
    RECENT = "recent"    # 6-15 years  
    MATURE = "mature"    # 16-30 years
    OLD = "old"          # 31+ years

class RentalStrategy(Enum):
    LONG_TERM = "long_term"
    SHORT_TERM = "short_term"
    HYBRID = "hybrid"

class LocationType(Enum):
    URBAN = "urban"
    SUBURBAN = "suburban"
    RURAL = "rural"
    VACATION = "vacation"

class ExpenseEstimate(NamedTuple):
    percentage: float
    description: str
    confidence: str  # "high", "medium", "low"
    source: str

class ExpenseFramework:
    """
    Comprehensive framework for estimating rental property expenses
    based on property characteristics and market conditions.
    """
    
    def __init__(self):
        self.maintenance_data = self._build_maintenance_framework()
        self.vacancy_data = self._build_vacancy_framework()
        self.management_data = self._build_management_framework()
        self.other_expenses_data = self._build_other_framework()
    
    def estimate_expenses(self, 
                         property_type: PropertyType,
                         property_age: PropertyAge,
                         rental_strategy: RentalStrategy,
                         location_type: LocationType,
                         property_value: float,
                         square_footage: int,
                         monthly_rent: float) -> Dict[str, ExpenseEstimate]:
        """
        Estimate all expense categories for a property.
        
        Args:
            property_type: Type of property
            property_age: Age category of property
            rental_strategy: Long-term, short-term, or hybrid
            location_type: Urban, suburban, rural, or vacation
            property_value: Current property value
            square_footage: Property square footage
            monthly_rent: Expected monthly rental income
            
        Returns:
            Dictionary with expense estimates for each category
        """
        
        return {
            'maintenance': self._estimate_maintenance(
                property_type, property_age, rental_strategy, property_value, square_footage, monthly_rent
            ),
            'vacancy': self._estimate_vacancy(
                rental_strategy, location_type, property_type
            ),
            'management': self._estimate_management(
                rental_strategy, location_type, monthly_rent
            ),
            'other': self._estimate_other(
                property_type, rental_strategy, location_type, monthly_rent
            )
        }
    
    def _build_maintenance_framework(self) -> Dict:
        """Build maintenance cost estimation framework"""
        return {
            # Base rates by property age (% of rent)
            'age_multipliers': {
                PropertyAge.NEW: 0.03,      # 3% for 0-5 years
                PropertyAge.RECENT: 0.06,   # 6% for 6-15 years
                PropertyAge.MATURE: 0.09,   # 9% for 16-30 years
                PropertyAge.OLD: 0.12       # 12% for 31+ years
            },
            
            # Property type adjustments
            'type_adjustments': {
                PropertyType.SINGLE_FAMILY: 1.0,      # Base rate
                PropertyType.DUPLEX: 1.1,             # +10% complexity
                PropertyType.MULTIFAMILY: 1.2,        # +20% systems complexity
                PropertyType.CONDO_TOWNHOME: 0.8      # -20% shared systems
            },
            
            # Rental strategy adjustments
            'strategy_adjustments': {
                RentalStrategy.LONG_TERM: 1.0,        # Base rate
                RentalStrategy.SHORT_TERM: 1.5,       # +50% turnover wear
                RentalStrategy.HYBRID: 1.25           # +25% mixed usage
            },
            
            # Alternative calculation methods
            'methods': {
                'percent_of_value': 0.01,              # 1% of property value annually
                'per_square_foot': 0.90,               # $0.90/sq ft annually (median)
                'percent_of_rent': 0.08                # 8% of rent (general rule)
            },
            
            'description': """
            Maintenance costs include routine repairs, preventive maintenance, and minor replacements.
            Based on 15,000+ work orders from 2024-2025: $0.62-$1.27 per sq ft annually.
            
            Key factors:
            - Property age is the primary driver (2-12% of rent)
            - STR properties require 50% more maintenance due to turnover
            - Mountain/vacation properties need extra weather protection
            - Deferred maintenance compounds quickly
            
            Best practices:
            - Budget conservatively for older properties
            - Track actual costs to refine estimates
            - Consider location-specific factors (weather, regulations)
            """,
            
            'confidence_factors': {
                'high': "Property <10 years, good maintenance history",
                'medium': "Property 10-25 years, average condition", 
                'low': "Property >25 years, unknown maintenance history"
            }
        }
    
    def _build_vacancy_framework(self) -> Dict:
        """Build vacancy rate estimation framework"""
        return {
            # National baseline: 7.1% (Q1 2025)
            'national_baseline': 0.071,
            
            # Rental strategy base rates
            'strategy_rates': {
                RentalStrategy.LONG_TERM: 0.06,       # 6% - stable tenants
                RentalStrategy.SHORT_TERM: 0.40,      # 40% - seasonal/turnover
                RentalStrategy.HYBRID: 0.15           # 15% - mixed strategy
            },
            
            # Location adjustments
            'location_adjustments': {
                LocationType.URBAN: 0.9,              # -10% high demand
                LocationType.SUBURBAN: 1.0,           # Base rate
                LocationType.RURAL: 1.3,              # +30% limited demand
                LocationType.VACATION: 1.2            # +20% seasonal variation
            },
            
            # Property type adjustments
            'type_adjustments': {
                PropertyType.SINGLE_FAMILY: 1.0,      # Base rate
                PropertyType.DUPLEX: 1.05,            # +5% coordination complexity
                PropertyType.MULTIFAMILY: 0.95,       # -5% professional mgmt
                PropertyType.CONDO_TOWNHOME: 0.9      # -10% amenities
            },
            
            'market_indicators': {
                'tight_market': {'rate': 0.04, 'description': 'Supply constrained, high demand'},
                'balanced_market': {'rate': 0.07, 'description': 'Normal supply/demand balance'},
                'soft_market': {'rate': 0.12, 'description': 'Oversupply, tenant market'}
            },
            
            'description': """
            Vacancy allowance accounts for periods between tenants and seasonal fluctuations.
            National rate: 7.1% (2025), but varies dramatically by strategy and location.
            
            Key considerations:
            - STR: High vacancy is normal (40-60%) due to seasonal demand
            - LTR: Target 5-8% in most markets
            - College towns: Higher seasonal variation
            - Vacation areas: Strong seasonality patterns
            - Economic factors: Employment, population growth
            
            Regional examples (2024-2025):
            - Austin, TX: 9.85% (oversupply)
            - Tampa, FL: 10%+ (new construction)
            - Memphis, TN: 9.4% (improving)
            """,
            
            'confidence_factors': {
                'high': "Local market data available, established rental history",
                'medium': "Regional data, similar property comparisons",
                'low': "Limited data, new market, economic uncertainty"
            }
        }
    
    def _build_management_framework(self) -> Dict:
        """Build property management fee framework"""
        return {
            # Base rates by rental strategy
            'strategy_rates': {
                RentalStrategy.LONG_TERM: {
                    'full_service': 0.10,      # 10% full service
                    'leasing_only': 0.06,      # 6% leasing only
                    'self_managed': 0.02       # 2% misc costs
                },
                RentalStrategy.SHORT_TERM: {
                    'full_service': 0.25,      # 25% average STR management
                    'half_service': 0.15,      # 15% marketing only
                    'self_managed': 0.05       # 5% platform fees, misc
                },
                RentalStrategy.HYBRID: {
                    'full_service': 0.18,      # 18% blended rate
                    'selective': 0.12,         # 12% seasonal help
                    'self_managed': 0.04       # 4% mixed costs
                }
            },
            
            # Location adjustments
            'location_adjustments': {
                LocationType.URBAN: 0.9,              # -10% more competition
                LocationType.SUBURBAN: 1.0,           # Base rate
                LocationType.RURAL: 1.3,              # +30% limited options
                LocationType.VACATION: 1.2            # +20% seasonal complexity
            },
            
            # Service level descriptions
            'service_levels': {
                'full_service': {
                    'ltr_includes': "Tenant screening, leasing, rent collection, maintenance coordination, legal compliance",
                    'str_includes': "Guest communication, dynamic pricing, cleaning coordination, maintenance, guest services"
                },
                'half_service': {
                    'ltr_includes': "Leasing and tenant placement only",
                    'str_includes': "Marketing and booking management, guest handles rest"
                },
                'self_managed': {
                    'description': "DIY management with third-party costs (software, legal, etc.)"
                }
            },
            
            'description': """
            Property management fees vary dramatically between LTR (6-13%) and STR (15-40%).
            STR requires much more intensive daily management.
            
            STR Management includes:
            - 24/7 guest communication
            - Dynamic pricing optimization  
            - Cleaning coordination (after each stay)
            - Maintenance and repairs
            - Guest services and local support
            
            LTR Management includes:
            - Tenant screening and placement
            - Rent collection and accounting
            - Maintenance coordination
            - Legal compliance and evictions
            
            Performance impact:
            - Professional STR management often increases revenue 18-20%
            - Good LTR management reduces vacancy and tenant issues
            """,
            
            'confidence_factors': {
                'high': "Multiple management companies available, clear pricing",
                'medium': "Some options available, market rates known",
                'low': "Limited management options, remote/rural location"
            }
        }
    
    def _build_other_framework(self) -> Dict:
        """Build framework for other expenses"""
        return {
            # Base rates by rental strategy (% of rent)
            'strategy_base_rates': {
                RentalStrategy.LONG_TERM: 0.04,       # 4% utilities, admin, etc.
                RentalStrategy.SHORT_TERM: 0.08,      # 8% utilities, supplies, admin
                RentalStrategy.HYBRID: 0.06           # 6% blended
            },
            
            # Detailed expense categories
            'categories': {
                'utilities': {
                    'ltr_rate': 0.01,          # 1% (tenant usually pays)
                    'str_rate': 0.03,          # 3% (owner pays all)
                    'hybrid_rate': 0.02        # 2% (seasonal variation)
                },
                'insurance_premium': {
                    'base_rate': 0.008,        # 0.8% of property value annually
                    'str_multiplier': 1.3,     # +30% for commercial coverage
                    'rural_multiplier': 1.2    # +20% for remote properties
                },
                'capex_reserves': {
                    'rate': 0.05,              # 5% for major replacements
                    'description': "HVAC, roof, flooring, appliances, etc."
                },
                'admin_costs': {
                    'ltr_rate': 0.005,         # 0.5% accounting, legal, etc.
                    'str_rate': 0.015,         # 1.5% software, accounting, legal
                    'includes': "Software, accounting, legal, licenses"
                },
                'supplies_amenities': {
                    'ltr_rate': 0.002,         # 0.2% minimal supplies
                    'str_rate': 0.015,         # 1.5% linens, toiletries, etc.
                    'includes': "Cleaning supplies, linens, toiletries, amenities"
                }
            },
            
            # Property type adjustments
            'type_adjustments': {
                PropertyType.SINGLE_FAMILY: 1.0,      # Base rate
                PropertyType.DUPLEX: 1.1,             # +10% shared systems
                PropertyType.MULTIFAMILY: 1.2,        # +20% common areas
                PropertyType.CONDO_TOWNHOME: 0.7      # -30% HOA covers some
            },
            
            'description': """
            Other expenses include utilities, insurance, CapEx reserves, admin costs, and supplies.
            Varies significantly between LTR (2-4% of rent) and STR (6-10% of rent).
            
            Key components:
            - Utilities: Owner responsibility in STR, tenant in LTR
            - CapEx reserves: 5% for major replacements (roof, HVAC, etc.)
            - Insurance: Commercial coverage for STR costs 30% more
            - Admin: Software, accounting, legal, licenses
            - STR supplies: Linens, toiletries, cleaning supplies
            
            Location factors:
            - Rural properties: Higher insurance, utility costs
            - Vacation areas: Seasonal utility spikes
            - HOA properties: Many expenses covered by association
            """,
            
            'confidence_factors': {
                'high': "Detailed expense history available",
                'medium': "Comparable properties analyzed",
                'low': "Limited data, new property type/location"
            }
        }
    
    def _estimate_maintenance(self, property_type: PropertyType, property_age: PropertyAge,
                            rental_strategy: RentalStrategy, property_value: float,
                            square_footage: int, monthly_rent: float) -> ExpenseEstimate:
        """Estimate maintenance costs"""
        data = self.maintenance_data
        
        # Base rate by age
        base_rate = data['age_multipliers'][property_age]
        
        # Apply adjustments
        type_adj = data['type_adjustments'][property_type]
        strategy_adj = data['strategy_adjustments'][rental_strategy]
        
        # Calculate final percentage
        percentage = base_rate * type_adj * strategy_adj
        
        # Cross-check with alternative methods
        value_method = (data['methods']['percent_of_value'] * property_value) / (monthly_rent * 12)
        sqft_method = (data['methods']['per_square_foot'] * square_footage) / (monthly_rent * 12)
        
        # Use conservative estimate (higher of calculated vs alternatives)
        percentage = max(percentage, value_method, sqft_method)
        
        # Determine confidence
        if property_age in [PropertyAge.NEW, PropertyAge.RECENT]:
            confidence = "high"
        elif property_age == PropertyAge.MATURE:
            confidence = "medium"
        else:
            confidence = "low"
        
        description = f"Based on {property_age.value} property, {rental_strategy.value} use. Industry data: ${data['methods']['per_square_foot']}/sq ft annually."
        
        return ExpenseEstimate(
            percentage=percentage,
            description=description,
            confidence=confidence,
            source="Industry data 2024-2025, 15,000+ work orders"
        )
    
    def _estimate_vacancy(self, rental_strategy: RentalStrategy, location_type: LocationType,
                         property_type: PropertyType) -> ExpenseEstimate:
        """Estimate vacancy rates"""
        data = self.vacancy_data
        
        # Base rate by strategy
        base_rate = data['strategy_rates'][rental_strategy]
        
        # Apply location adjustment
        location_adj = data['location_adjustments'][location_type]
        
        # Apply property type adjustment
        type_adj = data['type_adjustments'][property_type]
        
        # Calculate final percentage
        percentage = base_rate * location_adj * type_adj
        
        # Determine confidence based on strategy
        if rental_strategy == RentalStrategy.LONG_TERM:
            confidence = "high"
        elif rental_strategy == RentalStrategy.SHORT_TERM:
            confidence = "medium"  # More variable
        else:
            confidence = "medium"
        
        description = f"{rental_strategy.value.replace('_', ' ').title()} in {location_type.value} area. National average: {data['national_baseline']:.1%}"
        
        return ExpenseEstimate(
            percentage=percentage,
            description=description,
            confidence=confidence,
            source="National data Q1 2025, regional market analysis"
        )
    
    def _estimate_management(self, rental_strategy: RentalStrategy, location_type: LocationType,
                           monthly_rent: float) -> ExpenseEstimate:
        """Estimate management costs"""
        data = self.management_data
        
        # Assume full-service management for estimates
        base_rate = data['strategy_rates'][rental_strategy]['full_service']
        
        # Apply location adjustment
        location_adj = data['location_adjustments'][location_type]
        
        # Calculate final percentage
        percentage = base_rate * location_adj
        
        # Determine confidence
        if rental_strategy == RentalStrategy.LONG_TERM:
            confidence = "high"
        else:
            confidence = "medium"  # STR management more variable
        
        service_level = "full_service"
        includes = data['service_levels'][service_level][f'{rental_strategy.value}_includes'] if f'{rental_strategy.value}_includes' in data['service_levels'][service_level] else "Full property management services"
        
        description = f"Full-service management for {rental_strategy.value.replace('_', ' ')}. Includes: {includes[:100]}..."
        
        return ExpenseEstimate(
            percentage=percentage,
            description=description,
            confidence=confidence,
            source="Industry surveys 2024-2025, management company data"
        )
    
    def _estimate_other(self, property_type: PropertyType, rental_strategy: RentalStrategy,
                       location_type: LocationType, monthly_rent: float) -> ExpenseEstimate:
        """Estimate other expenses"""
        data = self.other_expenses_data
        
        # Base rate by strategy
        base_rate = data['strategy_base_rates'][rental_strategy]
        
        # Apply property type adjustment
        type_adj = data['type_adjustments'][property_type]
        
        # Calculate final percentage
        percentage = base_rate * type_adj
        
        # Add location premium for rural/vacation
        if location_type in [LocationType.RURAL, LocationType.VACATION]:
            percentage *= 1.1  # +10% for remote locations
        
        confidence = "medium"  # Generally good data available
        
        description = f"Utilities, insurance, CapEx reserves, admin costs. {rental_strategy.value.replace('_', ' ').title()} strategy."
        
        return ExpenseEstimate(
            percentage=percentage,
            description=description,
            confidence=confidence,
            source="Expense analysis 2024-2025, IRS data, industry standards"
        )

# Example usage and testing
if __name__ == "__main__":
    framework = ExpenseFramework()
    
    # Test with Eagle Drive property (duplex, older, LTR)
    print("=== EAGLE DRIVE DUPLEX (LTR) ===")
    eagle_estimates = framework.estimate_expenses(
        property_type=PropertyType.DUPLEX,
        property_age=PropertyAge.OLD,  # 1973 = 52 years old
        rental_strategy=RentalStrategy.LONG_TERM,
        location_type=LocationType.SUBURBAN,
        property_value=950000,
        square_footage=3964,
        monthly_rent=5400
    )
    
    for category, estimate in eagle_estimates.items():
        print(f"{category.upper()}: {estimate.percentage:.1%} - {estimate.description}")
    
    print("\n" + "="*50)
    
    # Test with Banner Elk property (single family, newer, STR)
    print("=== BANNER ELK HOUSE (STR) ===")
    banner_estimates = framework.estimate_expenses(
        property_type=PropertyType.SINGLE_FAMILY,
        property_age=PropertyAge.MATURE,  # 2004 = 21 years old
        rental_strategy=RentalStrategy.SHORT_TERM,
        location_type=LocationType.VACATION,
        property_value=560000,
        square_footage=2040,
        monthly_rent=4237
    )
    
    for category, estimate in banner_estimates.items():
        print(f"{category.upper()}: {estimate.percentage:.1%} - {estimate.description}")