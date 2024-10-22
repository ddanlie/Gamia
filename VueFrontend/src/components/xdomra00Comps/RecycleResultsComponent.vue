

<template>
    <!-- results window -->
    <div v-if="this.results" class="flex textCenter resStyle">

        <div class="scrolledHistory">
            <div v-if="this.nextSetRecord >= 0" 
                v-for="(playerName, idx) in this.results[this.playedSet].names.slice(0, this.nextSetRecord)"
                class="full three">
    
                <h3 class="full"
                    style="padding: 5% 0 5% 5%; text-align:left; color:black;">
                    {{playerName}}:<br/>{{this.results[this.playedSet].prompts[idx]}}
                </h3>
    
                <img class="full off-third" 
                    :src="this.results[this.playedSet].generatedSrc[idx]" 
                    style="max-height: 100vh; max-width: 100%; width: 200px; height: 200px; margin: 0% -55% 0 0 ;
                    object-fit: contain" :style="{ opacity: this.results[this.playedSet].generatedSrc[idx]==='' ? '1' : '1'}">
            </div>
        </div>


       
        
        <div class="full three" style="padding: 0 15% 5% 15%;">
            <button class="off-two redBack" :disabled="this.playedSet == 0" @click="this.prevSet">
                Prev
            </button>
            <button class="off-third -greenBack"  :disabled="this.playedSet == this.results.length-1" @click="this.nextSet">
                Next
            </button>
        </div>
    </div>

</template>


<script>
    import { getCurrentInstance } from 'vue'; 

    export default {
         
        props: {
            gameId: {
                required: true
            }
        },
        watch:
        {
        },

        mounted()
        {
            this.mounted = true;
            this.getResults();
        },

        unmounted()
        {
            this.mounted = false;
            clearInterval(this.revealInterval);
        },

        data()
        {
            return {
                results: null,
                mounted: false,
                //nested counters:
                playedSet: 0,//players - switch with buttons (show first player histrory, then next)
                nextSetRecord: undefined,//players history unit (show first generation, then another)        
                maxSubRecords: 2,
                revealInterval: undefined,
            }

        },

        methods: {

            getResults()
            {
                if(!this.mounted)
                    return;

                this.$api.get("recycle_game_results", {
                    params: {
                        gameId: this.gameId
                    }

                })
                .then(response => {
                    this.results = response.data.results;//array
                    console.log("RESULTS: "+this.results);
                    this.playedSet = 0;
                    this.startShow();
                })
                .catch(error => {
                    setTimeout(this.getResults, 2000);
                })
            }, 

            startShow()
            {
                this.nextSetRecord = -1;
                this.revealInterval = setInterval(this.revealNext, 100);
            },

            nextSet()
            {
                this.playedSet++;
                if(this.playedSet >= this.results.length)
                    this.playedSet = this.results.length-1;

                this.startShow();
            },

            prevSet()
            {
                this.playedSet--;
                if(this.playedSet < 0)
                    this.playeedSet = 0;

                this.startShow();
            },

            revealNext()
            {
                if(!this.mounted)
                    return;

                this.nextSetRecord++;
                if(this.nextSetRecord > this.results[this.playedSet].users.length)
                {
                    clearInterval(this.revealInterval);
                }
            }

        }
    }

</script>

<style scoped>

.resStyle
{
    max-width: 70%;
    background-color: white;
    border-radius: 15px;
}   

.scrolledHistory
{
    max-height: 100%;
}



</style>