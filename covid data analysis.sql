SELECT  *FROM `atomic-horizon-391421.coviddeath.covideath` 
where continent is not null
order by 3,4;

SELECT  *FROM `atomic-horizon-391421.coviddeath.covidvacc`
where continent is not null
order by 3,4;
--total cases vs total death 
--finding out the liklihood of dying in ur country if u contract covid

select location,date, total_cases,total_deaths,(total_deaths/total_cases)*100 as dying_percentage
from `atomic-horizon-391421.coviddeath.covideath` 
where location='India'
order by 1,2;


--total cases vs population
--finding the % of population inflicted on each date

select location,date, total_cases, population,(total_cases/population)*100 as inflict_percentage
from `atomic-horizon-391421.coviddeath.covideath` 

order by 1,2;

-- total cases vs population country wise
select location,sum( new_cases) total_cases, population,(sum(new_cases)/population)*100 as inflict_percentage
from `atomic-horizon-391421.coviddeath.covideath` 
group by location,population;


--finding countries with highest infection rate vs population

select location,population,date, max(total_cases) as highestinfectioncount, max((total_cases/population))*100 as inflict_percentage
from `atomic-horizon-391421.coviddeath.covideath` 
group by location,population,date
order by 4 desc;

--countries with highest death count

select location, max(total_deaths) as max_deaths
from `atomic-horizon-391421.coviddeath.covideath` 
where continent is not null
group by location
order by 2 desc;

--BREAKING THINGS BY CONTINENT
--CONTINENTS with highest death count

--this will give wrong insights due to fault in dataset
select continent , max(total_deaths) as max_deaths
from `atomic-horizon-391421.coviddeath.covideath` 
where continent is not null
group by continent
order by 2 desc;
--correct insight
select location, max(total_deaths) as max_deaths
from `atomic-horizon-391421.coviddeath.covideath` 
where continent is  null
group by location
order by 2 desc;


--GLOBAL NOS.

select SUM(new_cases) as total_cases,sum(new_deaths) as total_deaths ,(sum(new_deaths)/sum(new_cases))*100 as death_percentage
from `atomic-horizon-391421.coviddeath.covideath` 
where continent is not null
order by 1,2 desc;


--TOTAL POPULATION VS VACCINATIONS
--shows % of people who have recived at least one covid vacc

select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(vac.new_vaccinations) over(partition by dea.location order by dea.location , dea.date) as rollingpeoplevacc,
(sum(vac.new_vaccinations) over(partition by dea.location order by dea.location , dea.date))/(population)*100 as rollingpeoplevaccPercent
from  `coviddeath.covideath` as dea
join `coviddeath.covidvacc` as vac 
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
order by 2,3;

--using ctes

With  PopvsVac 
as
(
select dea.continent as coninent,dea.location location,dea.date date,dea.population population,vac.new_vaccinations new_vaccinations,
sum(vac.new_vaccinations) over(partition by dea.location order by dea.location,dea.date ) as rollingpeoplevacc

from  `coviddeath.covideath` as dea
join `coviddeath.covidvacc` as vac 
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
)
Select *, (RollingPeopleVacc/Population)*100 as percentPopVacc,
From PopvsVac
order by rollingpeoplevacc;
 
 --creating a view

 create view `coviddeath.percentPopulationVaccinated` as
 select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations,
sum(vac.new_vaccinations) over(partition by dea.location order by dea.location , dea.date) as rollingpeoplevacc,
(sum(vac.new_vaccinations) over(partition by dea.location order by dea.location , dea.date))/(population)*100 as rollingpeoplevaccPercent
from  `coviddeath.covideath` as dea
join `coviddeath.covidvacc` as vac 
on dea.location=vac.location and dea.date=vac.date
where dea.continent is not null
order by 2,3;

drop view `coviddeath.percentPopulationVaccinated`;

Select location, SUM(new_deaths) as TotalDeathCount
From `coviddeath.covideath`
--Where location like '%states%'
Where continent is null 
and location not in ('World', 'European Union', 'International')
Group by location
order by TotalDeathCount desc

