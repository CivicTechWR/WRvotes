
RESULT_ACCLAIMED = "Acclaimed"
RESULT_WINNER = "Winner"
RESULT_WITHDRAWN = "Withdrawn"

module WRVotes
  class NomineesResultsGenerator < Jekyll::Generator
    safe true
    priority :low

    def votes_to_i(v, v_default)
        return (v.nil? || v.to_s.strip.empty?) ? v_default : v.to_i
    end

    def determine_race_scale(group, number_to_elect)
      total_votes = 0
      max_votes = 0
      group.each do |nominee|
        votes = votes_to_i(nominee['Votes'], 0)
        total_votes += votes
        max_votes = [max_votes, votes].max()
      end

      if number_to_elect > 1
        return max_votes
      else
        return total_votes
      end
    end

    def generate(site)
      nominees  = site.data.dig('sync', 'nominees')


      unless nominees 
        Jekyll.logger.warn 'NomineesResultsGenerator:', \
          'site.data.sync.nominees not found; skipping.'
        return
      end

      grouped_by_race = nominees.group_by { |n| n['PositionUniqueName'] }

      sorted_nominees_results = {}
      grouped_by_race.each do |race_id, group|
        next if race_id.nil? || race_id.empty?

        race = site.data.dig('internal','position-tags').find do |r|
          r['PositionUniqueName'] == race_id
        end

        vote_scale = determine_race_scale(group, race['NumberToElect'].to_i)
        group.each do |nominee|
          nominee['Vote_scale'] = vote_scale
        end

        group = group.filter do |nominee|
          not(nominee['Withdrawn'] == "Y" and votes_to_i(nominee['Votes'], -1) == 0)
        end

        sorted_nominees_results[race_id] = group.sort_by do |nominee|
          -votes_to_i(nominee['Votes'], -1)
        end
      end

      site.data['sorted_nominees_results'] = sorted_nominees_results
      Jekyll.logger.info 'NomineesResultsGenerator:', \
        "Built sorted_nominees for #{sorted_nominees_results.keys.size} races."
    end
  end
end